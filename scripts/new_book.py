#!/usr/bin/env python3
"""Scaffold a single hand-written book spec under books/<genre>/<slug>/book.json.

Example:
  python scripts/new_book.py --title "The Salt Cathedral" --genre fantasy \
      --author "Ines Voss" --length novel --rating 4.5 \
      --blurb "A cathedral carved from salt ..." --themes faith,family
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_catalog import GENRES, slugify  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--title", required=True)
    parser.add_argument("--blurb", required=True)
    parser.add_argument("--genre", required=True,
                        help=f"shelf name: {', '.join(GENRES)}")
    parser.add_argument("--author", default="Anonymous")
    parser.add_argument("--length", default="novel",
                        choices=["short-story", "novella", "novel", "epic"])
    parser.add_argument("--rating", type=float, default=None)
    parser.add_argument("--chapters", type=int, default=None)
    parser.add_argument("--words-per-chapter", type=int, default=None)
    parser.add_argument("--themes", default="", help="comma-separated")
    parser.add_argument("--style", default="")
    parser.add_argument("--language", default="English")
    args = parser.parse_args()

    genre_key = slugify(args.genre)
    if genre_key not in GENRES:
        print(f"Unknown shelf '{args.genre}'. Known: {', '.join(GENRES)}",
              file=sys.stderr)
        return 1

    slug = slugify(args.title)
    folder = ROOT / "books" / genre_key / slug
    spec_path = folder / "book.json"
    if spec_path.exists():
        print(f"Refusing to overwrite {spec_path}", file=sys.stderr)
        return 1

    spec = {
        "title": args.title,
        "author": args.author,
        "genre": GENRES[genre_key]["label"],
        "length": args.length,
        "rating": args.rating,
        "blurb": args.blurb.strip(),
        "themes": [t.strip() for t in args.themes.split(",") if t.strip()],
        "style": args.style,
        "language": args.language,
    }
    if args.chapters:
        spec["chapters"] = args.chapters
    if args.words_per_chapter:
        spec["words_per_chapter"] = args.words_per_chapter

    folder.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print(f"Wrote {spec_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
