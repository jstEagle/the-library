# The Library

An entire library of books, written by AI, stored as markdown, and readable
straight from this repo. Every book is generated from a small JSON
description (title, blurb, genre, length...) via [OpenRouter](https://openrouter.ai),
a few chapters at a time, thousands of books in parallel.

**Read:** browse [`books/`](books/) — every finished book has a `README.md`
landing page with its table of contents. GitHub renders everything.

---

## Repo layout

```
the-library/
├── config.json               # the set model ID + generation settings
├── .env                      # OPENROUTER_API_KEY (gitignored — create from .env.example)
├── scripts/
│   ├── generate.py           # parallel generator (outlines → chapters → landing pages)
│   ├── make_catalog.py       # deterministic bulk spec generator (built the 10k catalog)
│   └── new_book.py           # scaffold one hand-written book spec
└── books/
    ├── fantasy/
    │   └── the-last-garden/
    │       ├── book.json     # human/catalog-authored description (the only input)
    │       ├── outline.json  # generated chapter plan (resume anchor)
    │       ├── 00-front-matter.md
    │       ├── 01-the-doorway.md   # chapters, in order
    │       ├── 02-....md
    │       └── README.md     # landing page + TOC, written when complete
    ├── science-fiction/…
    └── …10 genre shelves, 10,000 books total
```

## Quickstart

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env                  # add your OpenRouter key

# pilot: one shelf
.venv/bin/python scripts/generate.py --book fantasy --dry-run
.venv/bin/python scripts/generate.py --book fantasy

# everything pending (safe to Ctrl+C and re-run anytime; it resumes)
.venv/bin/python scripts/generate.py
```

The model is configured once in `config.json` (`"model"`), and can be
overridden per run (`--model`) or per book (`"model"` field in a book's JSON).

## Commands

### `scripts/generate.py` — write the books

| flag | effect |
|---|---|
| *(none)* | generate all pending outlines + missing chapters |
| `--book SUBSTR` | restrict to slugs containing SUBSTR (repeatable). Slugs are `<genre>/<title>` so `--book fantasy` = whole shelf |
| `--list` | status table of every book |
| `--dry-run` | print request/word estimates without calling the API |
| `--workers N` | override max concurrent API requests (default 32) |
| `--model ID` | override the configured model for this run |
| `--force` | delete generated files of the selection and regenerate |

Existing files are never rewritten; each run picks up exactly where the last
one stopped.

### `scripts/make_catalog.py` — build the catalog

Deterministic: book *i* depends only on `--seed` and *i*, so re-running or
growing the library never churns existing specs, and hand-written specs are
never touched.

```bash
python3 scripts/make_catalog.py --count 10000        # what's in the repo now
python3 scripts/make_catalog.py --count 250          # small batch
python3 scripts/make_catalog.py --genres horror,fantasy --count 500
```

### `scripts/new_book.py` — add one book by hand

```bash
python3 scripts/new_book.py --title "The Salt Cathedral" --genre fantasy \
    --author "Ines Voss" --length novel --rating 4.5 \
    --blurb "A cathedral carved from salt is slowly weeping away..." \
    --themes faith,family,decay
```

## The book spec

Every book starts as a folder with a `book.json`:

```jsonc
{
  "title": "The Rough Trail",
  "author": "Bram Delacroix",            // fictional pen name
  "genre": "Adventure",                  // display label
  "length": "novella",                   // short-story | novella | novel | epic
  "rating": 4.4,                         // shown as stars on landing pages
  "blurb": "Elodie Winterbourne, a railroad engineer…",
  "themes": ["inheritance", "identity"], // steer the outline
  "style": "vivid, cinematic prose",     // optional prose guidance
  "language": "English",
  "chapters": 12,                        // optional override of the length preset
  "words_per_chapter": 2000,             // optional override
  "model": null                          // optional per-book model override
}
```

Length presets live in `config.json`. Only `title`, `blurb`, and resolvable
length are required.

## How generation works

1. **Outline** — one call expands the blurb into a premise, a fictional author
   bio, and N chapter summaries (saved to `outline.json`; the resume anchor).
2. **Chapters** — every missing chapter across *all* selected books flows
   through one global work queue with `--workers` concurrent streamed calls.
   Each writer sees the full plan plus the tail of the previous chapter for
   continuity, and writes atomically.
3. **Landing page** — when a book's last chapter lands, its `README.md`
   (metadata, star rating, word count, TOC) is written.

Robustness at scale: streaming requests, exponential backoff honoring
`Retry-After`, instant failure on non-retryable 4xx, truncated-JSON repair +
sanitization for reasoning models, content-level retries for malformed
outlines, and atomic writes everywhere.

## Scale & cost reality check

The full catalog is **10,000 books ≈ 224k chapter requests ≈ 500M words**.
Even at ~35 outline-calls/min you're looking at hours for outlines alone and
days-to-weeks of continuous generation for all chapters, plus whatever your
model charges per token. Practical patterns:

- generate one shelf at a time: `generate.py --book mystery`
- use a cheap/fast model for bulk: `generate.py --model google/gemini-2.0-flash-001`
- monitor: `tail -f generation.log` / `generate.py --list | grep -v complete`
- stop anytime with Ctrl+C (or `pkill -f scripts/generate.py`) — re-running resumes

Run it under `caffeinate -i …` on macOS so sleep doesn't pause long runs.

## Status of this repo

- [x] Catalog: 10,000 specs across 10 shelves (`make_catalog.py --seed 2026`)
- [ ] Full generation: **in progress** — track with `scripts/generate.py --list`

*All authors, books, and events herein are fictional. Everything is
machine-generated.*
