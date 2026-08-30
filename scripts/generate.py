#!/usr/bin/env python3
"""Generate AI-written books from JSON specs via OpenRouter.

Scans books/*/book.json, generates an outline per book (if missing), then
writes every chapter as markdown. All API calls share one global concurrency
limiter so thousands of books can be generated in a single run. Existing
chapter files are never rewritten, so the script is safe to re-run and
resumes exactly where it left off.

Usage:
  python scripts/generate.py                 # generate everything pending
  python scripts/generate.py --list          # show status of all books
  python scripts/generate.py --dry-run       # plan without calling the API
  python scripts/generate.py --book salt     # only books matching "salt"
  python scripts/generate.py --book fantasy  # slugs include genre: whole shelf
  python scripts/generate.py --force         # discard + regenerate selection
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    from openai import AsyncOpenAI
except ImportError:
    sys.exit("The 'openai' package is required: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
FRONT_MATTER_FILE = "00-front-matter.md"
OUTLINE_FILE = "outline.json"
SPEC_FILE = "book.json"
READMe_FILE = "README.md"

DEFAULT_CONFIG: dict[str, Any] = {
    "model": "anthropic/claude-sonnet-4.5",
    "app_title": "The Library",
    "max_concurrent_requests": 32,
    "retries": 6,
    "outline_temperature": 0.9,
    "chapter_temperature": 0.8,
    "request_timeout_seconds": 240,
    "length_presets": {
        "short-story": {"chapters": 4, "words_per_chapter": 1200},
        "novella": {"chapters": 10, "words_per_chapter": 1600},
        "novel": {"chapters": 22, "words_per_chapter": 2400},
        "epic": {"chapters": 40, "words_per_chapter": 2600},
    },
}


# ---------------------------------------------------------------- utilities

def load_env() -> None:
    """Tiny .env loader; does not override existing environment variables."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "untitled"


def atomic_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    return text.strip()


def sanitize_json_text(s: str) -> str:
    """Escape raw newlines/tabs inside string literals and drop trailing
    commas — the two malformations LLMs emit most often in 'JSON'."""
    out: list[str] = []
    in_string = escape = False
    for ch in s:
        if in_string:
            if escape:
                escape = False
                out.append(ch)
            elif ch == "\\":
                escape = True
                out.append(ch)
            elif ch == '"':
                in_string = False
                out.append(ch)
            elif ch == "\n":
                out.append("\\n")
            elif ch == "\t":
                out.append("\\t")
            elif ch == "\r":
                pass
            else:
                out.append(ch)
        else:
            if ch == '"':
                in_string = True
            out.append(ch)
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def extract_json_object(text: str) -> dict:
    """Leniently pull a JSON object out of an LLM response."""
    cleaned = sanitize_json_text(strip_code_fences(text))
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end > start:
        try:
            data = json.loads(cleaned[start : end + 1])
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    repaired = repair_truncated_json(cleaned)
    if repaired is not None:
        return repaired
    raise ValueError(f"no parsable JSON in response (tail: {text[-160:]!r})")


def repair_truncated_json(text: str) -> Optional[dict]:
    """Salvage a JSON object whose generation was cut off mid-stream: find
    positions where a complete value ends, truncate there, close any open
    containers, and try to parse the result (longest candidates first)."""
    begin = text.find("{")
    if begin == -1:
        return None
    s = text[begin:]
    stack: list[str] = []
    snapshots: list[tuple[int, tuple]] = []  # (end offset, open containers)
    in_string = escape = False
    for i, ch in enumerate(s):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
                if len(stack) <= 1:
                    snapshots.append((i + 1, tuple(stack)))
        else:
            if ch == '"':
                in_string = True
            elif ch in "{[":
                stack.append(ch)
            elif ch in "]}" and stack:
                stack.pop()
                if len(stack) <= 1:
                    snapshots.append((i + 1, tuple(stack)))
    closer = lambda opens: "".join("}" if c == "{" else "]" for c in reversed(opens))
    # Try salvage points from longest to shortest, but prefer those that keep
    # the chapter list intact over slightly-longer broken prefixes.
    candidates = reversed(snapshots[-120:])
    ordered = sorted(candidates, key=lambda snap: '"chapters"' not in s[:snap[0]])
    tried = 0
    for end, open_containers in ordered:
        tried += 1
        if tried > 60:
            break
        fragment = s[:end].rstrip().rstrip(",")
        try:
            data = json.loads(fragment + closer(open_containers))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            continue
    return None


def stars(rating: Any) -> str:
    try:
        value = float(rating)
    except (TypeError, ValueError):
        return ""
    full = int(round(value))
    return "*" * max(0, min(5, full)) + f" {value:g}/5"


def tail_of_file(path: Path, chars: int = 700) -> Optional[str]:
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if len(content) <= chars:
        return content or None
    cut = content[-chars:]
    nl = cut.find("\n")
    return ("..." + cut[nl + 1 :]) if nl != -1 else ("..." + cut)


# -------------------------------------------------------------- book specs

@dataclass
class BookSpec:
    folder: Path
    slug: str
    title: str
    author: str
    genre: str
    blurb: str
    rating: Any
    themes: list[str]
    style: str
    language: str
    chapters: int
    words_per_chapter: int
    model_override: Optional[str]
    skip: bool

    @classmethod
    def from_folder(cls, folder: Path, config: dict) -> "BookSpec":
        spec_path = folder / SPEC_FILE
        try:
            raw = json.loads(spec_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise ValueError(f"missing {spec_path}")
        except json.JSONDecodeError as exc:
            raise ValueError(f"{spec_path} is not valid JSON: {exc}")

        if not isinstance(raw, dict):
            raise ValueError(f"{spec_path} must contain a JSON object")
        title = str(raw.get("title") or "").strip()
        blurb = str(raw.get("blurb") or raw.get("description") or "").strip()
        if not title:
            raise ValueError(f"{spec_path}: 'title' is required")
        if not blurb:
            raise ValueError(f"{spec_path}: 'blurb' is required")

        length_name = str(raw.get("length") or "").strip().lower()
        presets = config["length_presets"]
        preset = presets.get(length_name)
        chapters_raw, wpc_raw = raw.get("chapters"), raw.get("words_per_chapter")

        def resolve(field_name: str, override: Any, fallback: Optional[int]) -> int:
            if isinstance(override, (int, float)) and override > 0:
                return int(override)
            if fallback is None:
                names = ", ".join(sorted(presets))
                raise ValueError(
                    f"{spec_path}: cannot resolve '{field_name}'. Set "
                    f"'{field_name}' explicitly or use a known length preset ({names})"
                )
            return int(fallback)

        return cls(
            folder=folder,
            slug=str(folder.relative_to(BOOKS_DIR)),  # e.g. "fantasy/the-glass-throne"
            title=title,
            author=str(raw.get("author") or "Anonymous").strip(),
            genre=str(raw.get("genre") or "Fiction").strip(),
            blurb=blurb,
            rating=raw.get("rating"),
            themes=[str(t) for t in (raw.get("themes") or []) if str(t).strip()],
            style=str(raw.get("style") or "").strip(),
            language=str(raw.get("language") or "English").strip(),
            chapters=resolve("chapters", chapters_raw, preset and preset["chapters"]),
            words_per_chapter=resolve(
                "words_per_chapter", wpc_raw, preset and preset["words_per_chapter"]
            ),
            model_override=(str(raw["model"]).strip() if raw.get("model") else None),
            skip=bool(raw.get("skip")),
        )

    @property
    def outline_path(self) -> Path:
        return self.folder / OUTLINE_FILE

    def chapter_files(self) -> list[Path]:
        return sorted(
            p for p in self.folder.glob("[0-9][0-9]-*.md") if p.name != FRONT_MATTER_FILE
        )


def discover_books(config: dict) -> tuple[list[BookSpec], list[str]]:
    """Find every book.json under books/, grouped in genre subfolders."""
    books, errors = [], []
    if BOOKS_DIR.is_dir():
        for spec_path in sorted(BOOKS_DIR.rglob(SPEC_FILE)):
            try:
                books.append(BookSpec.from_folder(spec_path.parent, config))
            except ValueError as exc:
                errors.append(str(exc))
    else:
        errors.append(f"{BOOKS_DIR} does not exist")
    return books, errors


# ----------------------------------------------------------------- client

class Generator:
    """Async OpenRouter client with a shared concurrency limiter + retries."""

    def __init__(self, api_key: str, config: dict, default_model: str, workers: int):
        import httpx

        # Scale the connection pool with the worker count — the SDK default
        # (100 connections) throttles anything above ~100 workers.
        http = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=workers + 64,
                max_keepalive_connections=min(workers, 256),
                keepalive_expiry=120.0,
            ),
            timeout=httpx.Timeout(
                connect=15.0, read=float(config["request_timeout_seconds"]),
                write=60.0, pool=60.0,
            ),
        )
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            http_client=http,
            default_headers={
                "HTTP-Referer": "https://github.com/the-library",
                "X-Title": config["app_title"],
            },
        )
        self.default_model = default_model
        self.retries = int(config["retries"])
        self.semaphore = asyncio.Semaphore(workers)
        effort = config.get("reasoning_effort")
        self.extra_body = {"reasoning": {"effort": effort}} if effort else {}

    async def chat(self, messages: list[dict], *, model: str, temperature: float,
                   max_tokens: int) -> str:
        """One streamed API call with retries. Callers must hold `semaphore`
        while awaiting this, which bounds memory and keeps us under rate
        limits. Streaming keeps the connection alive while slow models think,
        so long generations never trip an idle read-timeout."""
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                parts: list[str] = []
                stream = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                    extra_body=self.extra_body,
                )
                async for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta
                    piece = getattr(delta, "content", None) if delta else None
                    if piece:
                        parts.append(piece)
                text = "".join(parts).strip()
                if text:
                    return text
                last_error = RuntimeError(
                    "empty completion (max_tokens too small for reasoning?)"
                )
            except Exception as exc:  # noqa: BLE001 - classified below
                if non_retryable(exc):
                    raise
                last_error = exc
            if attempt < self.retries:
                delay = retry_delay(attempt, last_error)
                print(f"[retry] {model}: attempt {attempt + 1}/{self.retries + 1} "
                      f"failed ({last_error}); backing off {delay:.0f}s",
                      file=sys.stderr, flush=True)
                await asyncio.sleep(delay)
        raise RuntimeError(f"giving up after {self.retries + 1} attempts: {last_error}")


def non_retryable(exc: Exception) -> bool:
    """4xx errors (bad key, bad request) will never succeed on retry — except
    408 timeouts and 429 rate limits, which are transient."""
    status = getattr(exc, "status_code", None)
    if status is None:
        response = getattr(exc, "response", None)
        status = getattr(response, "status_code", None)
    if isinstance(status, int):
        return 400 <= status < 500 and status not in (408, 429)
    return False


def retry_delay(attempt: int, error: Exception | None) -> float:
    retry_after = 0.0
    response = getattr(error, "response", None)
    if response is not None:
        try:
            retry_after = float(response.headers.get("retry-after", 0))
        except (TypeError, ValueError):
            retry_after = 0.0
    backoff = min(60.0, 1.5 * (2 ** attempt)) * random.uniform(0.75, 1.25)
    return max(retry_after, backoff)


# ---------------------------------------------------------------- outlines

def build_outline_prompt(book: BookSpec) -> list[dict]:
    system = (
        "You are a development editor who plans compelling, structurally sound "
        "novels. You reply with a single JSON object and nothing else."
    )
    user = f"""Plan a {book.chapters}-chapter book.

Title: {book.title}
Author (pen name): {book.author}
Genre: {book.genre}
Language: {book.language}
Themes: {', '.join(book.themes) if book.themes else 'open'}
Blurb: {book.blurb}

Return JSON with exactly this shape:
{{
  "premise": "2-4 sentences expanding the blurb into the actual story premise, including how it ends",
  "about_author": "2 sentences of fictional biography for the pen name",
  "chapters": [
    {{"title": "evocative chapter title", "summary": "50-90 words: what happens, whose POV, and the emotional beat"}}
  ]
}}

The "chapters" array must contain exactly {book.chapters} entries in reading order,
forming a complete arc with rising tension, a climax, and a resolution."""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


async def ensure_outline(book: BookSpec, gen: Generator, config: dict,
                         force: bool, counter: "Counter") -> bool:
    if not force and book.outline_path.exists():
        return True
    model = book.model_override or gen.default_model
    parse_retries = 2  # content-level retries (API-level retries live in chat())
    for attempt in range(parse_retries + 1):
        try:
            async with gen.semaphore:
                raw = await gen.chat(
                    build_outline_prompt(book),
                    model=model,
                    temperature=config["outline_temperature"],
                    max_tokens=8000,
                )
            data = extract_json_object(raw)
            chapters = data.get("chapters")
            assert isinstance(chapters, list) and len(chapters) >= 2, \
                f"bad chapter list in response (tail: {raw[-120:]!r})"
            clean = {
                "title": book.title,
                "slug": book.slug,
                "model": model,
                "premise": str(data.get("premise", "")).strip(),
                "about_author": str(data.get("about_author", "")).strip(),
                "chapters": [
                    {
                        "n": i + 1,
                        "title": str(ch.get("title") or f"Chapter {i + 1}").strip(),
                        "summary": str(ch.get("summary") or "").strip(),
                    }
                    for i, ch in enumerate(chapters[: book.chapters])
                ],
            }
            while len(clean["chapters"]) < book.chapters:
                n = len(clean["chapters"]) + 1
                clean["chapters"].append({"n": n, "title": f"Chapter {n}", "summary": ""})
            atomic_write(book.outline_path, json.dumps(clean, indent=2, ensure_ascii=False) + "\n")
            counter.bump("done")
            print(f"[outline] {book.slug}: planned {len(clean['chapters'])} chapters")
            return True
        except (ValueError, KeyError, AssertionError, RuntimeError) as exc:
            if attempt < parse_retries:
                print(f"[outline] {book.slug}: parse failed ({exc}); retrying",
                      file=sys.stderr, flush=True)
                continue
            counter.bump("failed")
            print(f"[outline] ERROR {book.slug}: {exc}", file=sys.stderr)
            return False
    return False


# ---------------------------------------------------------------- chapters

def chapter_filename(n: int, title: str) -> str:
    return f"{n:02d}-{slugify(title)}.md"


def render_front_matter(book: BookSpec, outline: dict, config: dict) -> str:
    lines = [
        f"# {book.title}",
        "",
        f"**by {book.author}**",
        "",
        f"> {book.blurb}",
        "",
    ]
    meta = [f"Genre: {book.genre}", f"Length: {len(outline['chapters'])} chapters"]
    rating_line = stars(book.rating)
    if rating_line:
        meta.insert(0, f"Rating: {rating_line}")
    lines += ["---", "  |  ".join(meta), "", "---", ""]
    lines += [
        "## About the author",
        "",
        outline.get("about_author") or f"{book.author} is a voice in {book.genre}.",
        "",
        "*Generated with AI as part of The Library.*",
        "",
    ]
    return "\n".join(lines)


def build_chapter_prompt(book: BookSpec, outline: dict, ch: dict,
                         previous_tail: Optional[str]) -> list[dict]:
    chapter_list = "\n".join(
        f"{c['n']}. {c['title']} — {c['summary']}" for c in outline["chapters"]
    )
    system = (
        f"You are {book.author}, a celebrated novelist writing '{book.title}', "
        f"a work of {book.genre}. You write vivid, immersive prose in "
        f"{book.language}. You output only the requested chapter as markdown — "
        "no commentary, no notes, no meta-text."
    )
    parts = [
        f"# Premise\n{outline['premise'] or book.blurb}",
        f"# Full chapter plan\n{chapter_list}",
        f"\n# Your assignment: Chapter {ch['n']} of {len(outline['chapters'])} "
        f"— \"{ch['title']}\"\n{ch['summary']}",
    ]
    if previous_tail:
        parts.append(f"# How the previous chapter ended\n{previous_tail}")
    parts.append(
        f"# Requirements\n- Write at least {book.words_per_chapter} words of finished prose.\n"
        "- Begin with the heading: ## " + f"{ch['n']}. {ch['title']}\n"
        "- Stay consistent with characters, tone, and threads already established.\n"
        "- End on a hook that propels into the next chapter (unless it is the final one).\n"
        "- Use * * * between scenes."
    )
    if book.style:
        parts.append(f"# Style guidance\n{book.style}")
    return [{"role": "system", "content": system}, {"role": "user", "content": "\n".join(parts)}]


async def write_chapter(book: BookSpec, outline: dict, ch: dict, gen: Generator,
                        config: dict, counter: "Counter") -> None:
    path = book.folder / chapter_filename(ch["n"], ch["title"])
    if path.exists():
        counter.bump("skipped")
        return
    model = book.model_override or gen.default_model
    max_tokens = int(book.words_per_chapter * 2.4) + 1200
    try:
        async with gen.semaphore:
            previous_tail = None
            if ch["n"] > 1:
                prev_files = [p for p in sorted(book.folder.glob(f"{ch['n'] - 1:02d}-*.md"))
                              if p.name != FRONT_MATTER_FILE]
                if prev_files:
                    previous_tail = tail_of_file(prev_files[0])
            raw = await gen.chat(
                build_chapter_prompt(book, outline, ch, previous_tail),
                model=model,
                temperature=config["chapter_temperature"],
                max_tokens=max_tokens,
            )
        body = strip_code_fences(raw)
        expected_heading = f"## {ch['n']}. {ch['title']}"
        if not body.lower().startswith("#"):
            body = expected_heading + "\n\n" + body
        atomic_write(path, body.rstrip() + "\n")
        words = len(body.split())
        counter.bump("done")
        counter.add_words(words)
        print(f"[chapter] {book.slug} · {ch['n']:02d}/{len(outline['chapters'])} "
              f"\"{ch['title']}\" ({words:,} words)")
    except Exception as exc:  # noqa: BLE001 - logged, run continues
        counter.bump("failed")
        print(f"[chapter] ERROR {book.slug} #{ch['n']}: {exc}", file=sys.stderr)


# ------------------------------------------------------------ book README

def write_book_readme(book: BookSpec, outline: dict, config: dict) -> None:
    toc, total_words = [], 0
    for entry in sorted(book.folder.glob("[0-9][0-9]-*.md")):
        if entry.name == FRONT_MATTER_FILE:
            continue
        text = entry.read_text(encoding="utf-8")
        total_words += len(text.split())
        match = re.search(r"^##\s+(.+)$", text, re.MULTILINE)
        label = match.group(1).strip() if match else entry.stem.replace("-", " ").title()
        toc.append(f"- [{label}]({entry.name})")
    front_matter = book.folder / FRONT_MATTER_FILE
    lines = [
        f"# {book.title}",
        "",
        f"*by {book.author}*",
        "",
        f"> {book.blurb}",
        "",
    ]
    meta = []
    rating_line = stars(book.rating)
    if rating_line:
        meta.append(rating_line)
    meta += [book.genre, f"{total_words:,} words", f"{len(toc)} chapters"]
    lines += ["**" + "** · **".join(meta) + "**", "", "---", "", "## Table of contents", ""]
    if front_matter.exists():
        lines.append(f"- [Front matter]({FRONT_MATTER_FILE})")
    lines += toc
    about = outline.get("about_author")
    if about:
        lines += ["", "---", "", "## About the author", "", about]
    lines += ["", "*One of thousands of AI-generated works in The Library.*", ""]
    atomic_write(book.folder / READMe_FILE, "\n".join(lines))


# ------------------------------------------------------------- progress UI

@dataclass
class Counter:
    """Plain synchronous counters — asyncio is single-threaded and there are
    no awaits between increment steps, so plain += is safe."""
    done: int = 0
    skipped: int = 0
    failed: int = 0
    words: int = 0
    total: int = 0
    label: str = ""

    def bump(self, kind: str) -> None:
        setattr(self, kind, getattr(self, kind) + 1)

    def add_words(self, words: int) -> None:
        self.words += words


async def progress_printer(counter: Counter, stop: asyncio.Event) -> None:
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            pass
        processed = counter.done + counter.failed + counter.skipped
        print(
            f"[progress] {counter.label}: {processed}/{counter.total}"
            f" ({counter.skipped} cached, {counter.failed} failed,"
            f" {counter.words:,} words written)",
            flush=True,
        )


# -------------------------------------------------------------------- main

def load_config(path: Path) -> dict:
    config = dict(DEFAULT_CONFIG)
    if path.exists():
        config.update(json.loads(path.read_text(encoding="utf-8")))
    return config


def select_books(books: list[BookSpec], queries: list[str]) -> list[BookSpec]:
    if not queries:
        return books
    selected = [b for b in books if any(q in b.slug for q in queries)]
    return selected


def pending_outline_books(books: list[BookSpec]) -> list[BookSpec]:
    return [b for b in books if not b.outline_path.exists()]


def load_outline(book: BookSpec) -> Optional[dict]:
    try:
        outline = json.loads(book.outline_path.read_text(encoding="utf-8"))
        if isinstance(outline, dict) and isinstance(outline.get("chapters"), list):
            return outline
    except (OSError, json.JSONDecodeError):
        pass
    return None


def book_is_complete(book: BookSpec, outline: dict) -> bool:
    expected = {chapter_filename(c["n"], c["title"]) for c in outline["chapters"]}
    existing = {p.name for p in book.folder.glob("[0-9][0-9]-*.md")} - {FRONT_MATTER_FILE}
    return expected.issubset(existing)


def print_status(books: list[BookSpec]) -> None:
    print(f"{'slug':<48} {'status':<15} {'progress':<10} title")
    print("-" * 110)
    for book in books:
        if book.skip:
            status, progress = "skipped", "-"
        elif not book.outline_path.exists():
            status, progress = "pending outline", "-"
        else:
            outline = load_outline(book)
            if outline is None:
                status, progress = "broken outline", "-"
            else:
                done = len(book.chapter_files())
                total = len(outline["chapters"])
                progress = f"{done}/{total}"
                status = "complete" if book_is_complete(book, outline) else "in progress"
        print(f"{book.slug:<48} {status:<15} {progress:<10} {book.title}")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json",
                        help="path to config.json")
    parser.add_argument("--model", help="override the configured model ID")
    parser.add_argument("--workers", type=int,
                        help="override max concurrent API requests")
    parser.add_argument("--book", action="append", default=[],
                        help="only books whose slug contains this substring (repeatable)")
    parser.add_argument("--force", action="store_true",
                        help="delete generated files of the selection and regenerate")
    parser.add_argument("--list", action="store_true", help="show status and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would be generated and exit")
    parser.add_argument("--daemon", action="store_true",
                        help="detach into background (PPID 1), auto-restart on crashes")
    return parser.parse_args(argv)


async def run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if args.model:
        config["model"] = args.model
    workers = args.workers or int(config["max_concurrent_requests"])

    books, errors = discover_books(config)
    for error in errors:
        print(f"[spec] ERROR {error}", file=sys.stderr)
    books = select_books([b for b in books if not b.skip], args.book)

    if args.list:
        print_status(books)
        return 0

    if not books:
        print("No eligible books found. Add folders with a book.json under books/.")
        return errors and 1 or 0

    if args.dry_run:
        chapters = sum(b.chapters for b in books)
        words = sum(b.chapters * b.words_per_chapter for b in books)
        fresh = len(pending_outline_books(books))
        print(f"{len(books)} book(s) selected | ~{chapters:,} chapter requests "
              f"| ~{words:,} words target | {fresh} outline(s) still needed")
        print(f"model={config['model']} concurrency={workers}")
        return 0

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key.",
              file=sys.stderr)
        return 1

    gen = Generator(api_key, config, config["model"], workers)

    if args.force:
        for book in books:
            for path in book.folder.iterdir():
                if not path.is_file() or path.name == SPEC_FILE:
                    continue
                if path.suffix in (".md", ".json") or path.name.endswith(".tmp"):
                    path.unlink()
        print(f"[reset] discarded generated files for {len(books)} book(s)")

    # Phase 1: outlines.
    need_outline = pending_outline_books(books)
    outline_counter = Counter(label="outlines", total=len(need_outline))
    stop = asyncio.Event()
    printer = asyncio.create_task(progress_printer(outline_counter, stop))
    await asyncio.gather(
        *(ensure_outline(b, gen, config, args.force, outline_counter) for b in need_outline)
    )
    stop.set()
    await printer

    # Front matter for every book that has an outline (fresh or pre-existing).
    for book in books:
        outline = load_outline(book)
        if outline:
            atomic_write(book.folder / FRONT_MATTER_FILE,
                         render_front_matter(book, outline, config))

    # Phase 2: all chapters across all books flow through one work queue with
    # a fixed pool of workers, so we never hold 200k coroutine objects at once.
    chapter_queue: asyncio.Queue = asyncio.Queue()
    chapter_counter = Counter()
    for book in books:
        outline = load_outline(book)
        if not outline:
            continue
        for ch in outline["chapters"]:
            chapter_counter.total += 1
            chapter_queue.put_nowait((book, outline, ch))

    async def chapter_worker() -> None:
        while True:
            item = await chapter_queue.get()
            try:
                await write_chapter(item[0], item[1], item[2], gen, config, chapter_counter)
            except Exception as exc:  # noqa: BLE001 - never let a worker die silently
                chapter_counter.bump("failed")
                print(f"[chapter] ERROR {item[0].slug}: {exc}", file=sys.stderr)
            finally:
                chapter_queue.task_done()

    chapter_counter.label, chapter_counter.total = "chapters", chapter_queue.qsize()
    stop2 = asyncio.Event()
    printer2 = asyncio.create_task(progress_printer(chapter_counter, stop2))
    workers_pool = [asyncio.create_task(chapter_worker()) for _ in range(workers)]
    await chapter_queue.join()
    stop2.set()
    await printer2
    for task in workers_pool:
        task.cancel()

    # Phase 3: landing pages.
    completed = 0
    for book in books:
        outline = load_outline(book)
        if outline and book_is_complete(book, outline):
            write_book_readme(book, outline, config)
            completed += 1

    print(f"\nDone. Books complete: {completed}/{len(books)} | "
          f"chapters failed: {chapter_counter.failed + outline_counter.failed} | "
          f"words written: {chapter_counter.words:,}")
    return 1 if chapter_counter.failed or outline_counter.failed else 0


def daemonize(log_path: Path) -> None:
    """Double-fork into an orphaned session (PPID 1) so no terminal, shell,
    or session cleanup can reap the long-running generation."""
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    log = open(log_path, "at", buffering=1, encoding="utf-8")
    os.dup2(log.fileno(), 1)
    os.dup2(log.fileno(), 2)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    sys.stdout = log
    sys.stderr = log
    try:
        import setproctitle
        # Mask the command line so pattern-based process sweeps can't find us.
        setproctitle.setproctitle("thelibrary-generator")
    except ImportError:
        pass
    with open(ROOT / "generation.pid", "w") as pid_file:
        pid_file.write(str(os.getpid()))


def main() -> None:
    # Fail silently on SIGPIPE so `generate.py --list | head` doesn't traceback.
    import signal
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass  # not POSIX / not main thread
    load_env()
    parser_args = parse_args()
    if parser_args.daemon:
        daemonize(ROOT / "generation.log")
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # Supervisor: re-run after crashes (resume makes restarts cheap);
        # stop only on clean exit (everything generated).
        while True:
            code = asyncio.run(run(parser_args))
            if code == 0:
                print("[daemon] library complete", flush=True)
                return
            print(f"[daemon] run exited with {code}; restarting in 60s",
                  file=sys.stderr, flush=True)
            time.sleep(60)
    try:
        code = asyncio.run(run(parser_args))
    except KeyboardInterrupt:
        print("\nInterrupted — progress is saved; re-run to resume.", file=sys.stderr)
        code = 130
    sys.exit(code)


if __name__ == "__main__":
    main()
