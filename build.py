#!/usr/bin/env python3
"""Regenerate sitemap.xml and llms-full.txt from the pages themselves.

Two derived files, one source of truth. Run after editing any page:

    python3 build.py

llms-full.txt is the whole site as plain text in one fetch. Assistants that will
read one file and not crawl five get everything; the per-page HTML is still there
for the ones that crawl.
"""
from __future__ import annotations
import re, pathlib, datetime
from html.parser import HTMLParser

SITE = "https://thyrowise.github.io"
ROOT = pathlib.Path(__file__).parent
SKIP_TAGS = {"script", "style", "svg", "nav", "head"}
BLOCK = {"p", "li", "h1", "h2", "h3", "div", "tr", "table", "ul", "ol"}


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []
        self.depth = 0          # inside a tag we ignore
        self.title = ""
        self.in_title = False
        self.cell: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.depth += 1
        if tag == "title":
            self.in_title = True
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.depth:
            self.depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.depth:
            return
        self.out.append(data)

    @property
    def text(self) -> str:
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return t.strip()


def pages() -> list[tuple[str, pathlib.Path]]:
    """(url path, file) for every page, homepage first."""
    found = []
    for f in sorted(ROOT.rglob("index.html")):
        rel = f.parent.relative_to(ROOT).as_posix()
        found.append(("/" if rel == "." else f"/{rel}/", f))
    found.sort(key=lambda p: (p[0] != "/", p[0]))
    return found


def main() -> None:
    today = datetime.date.today().isoformat()
    urls, chunks = [], []

    for path, f in pages():
        p = Text()
        p.feed(f.read_text(encoding="utf-8"))
        urls.append((path, "1.0" if path == "/" else "0.8"))
        chunks.append(f"# {p.title.strip()}\nURL: {SITE}{path}\n\n{p.text}\n")

    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(
            f"  <url>\n    <loc>{SITE}{u}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <priority>{pri}</priority>\n  </url>\n"
            for u, pri in urls
        )
        + "</urlset>\n",
        encoding="utf-8",
    )

    (ROOT / "llms-full.txt").write_text(
        "# Thyrowise — full site text\n"
        f"# Generated {today} from https://thyrowise.github.io. "
        "Structured index: https://thyrowise.github.io/llms.txt\n\n"
        + ("\n\n---\n\n".join(chunks))
        + "\n",
        encoding="utf-8",
    )

    print(f"sitemap.xml: {len(urls)} URL")
    print(f"llms-full.txt: {(ROOT / 'llms-full.txt').stat().st_size} bytes")


if __name__ == "__main__":
    main()
