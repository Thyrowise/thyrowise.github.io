#!/usr/bin/env python3
"""Sitenin adresini tek komutla değiştir.

    python3 set-url.py https://thyrowise.com

canonical, og:url, JSON-LD @id, llms.txt bağlantıları, robots.txt'teki sitemap
satırı ve build.py'deki SITE sabiti — hepsi tek yerden. Ücretsiz bir adreste
başlayıp sonradan kendi alan adına geçmek bu yüzden bir komut.
"""
from __future__ import annotations
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).parent
TARGETS = ["*.html", "*.txt", "*.xml", "build.py"]


def current() -> str:
    m = re.search(r'^SITE = "([^"]+)"', (ROOT / "build.py").read_text(encoding="utf-8"), re.M)
    if not m:
        sys.exit("build.py içinde SITE sabiti bulunamadı")
    return m.group(1)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(f"kullanım: python3 set-url.py https://yeni-adres\nşu an: {current()}")
    new = sys.argv[1].rstrip("/")
    if not new.startswith("https://"):
        sys.exit("adres https:// ile başlamalı")
    old = current()
    if old == new:
        sys.exit(f"zaten {old}")

    changed = 0
    for pat in TARGETS:
        for f in sorted(ROOT.rglob(pat)):
            t = f.read_text(encoding="utf-8")
            if old in t:
                f.write_text(t.replace(old, new), encoding="utf-8")
                changed += 1

    print(f"{old} → {new}  ({changed} dosya)")
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)


if __name__ == "__main__":
    main()
