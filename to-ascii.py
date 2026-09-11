#!/usr/bin/env python3
"""Sayfaları saf ASCII'ye çevir — görünen metni değiştirmeden.

Neden: GitHub'ın web editörüne kopyala-yapıştır, UTF-8 baytlarını tek baytlık
bir kodlama sanıp bozuyor (em dash -> ",Aî"). Her bayt 128'in altındaysa böyle
bir bozulma tanım gereği imkânsız.

Nasıl:
  HTML gövdesi     -> sayısal entity  (&#8212;)
  JSON-LD bloğu    -> JSON \\u kaçışı  (entity script içinde çözülmez)
  .txt dosyaları   -> ASCII karşılığı (entity düz metinde çözülmez)

Her dosya için, dönüşümden sonra anlamın birebir aynı kaldığı doğrulanır;
doğrulama düşerse dosya yazılmaz.

    python3 to-ascii.py            # tüm site
    python3 to-ascii.py faq/index.html
"""
from __future__ import annotations
import html, json, pathlib, re, sys

SCRIPT = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

# Düz metin dosyalarında entity çözülmez, o yüzden karşılığını yazıyoruz.
PLAIN = {"—": "--", "–": "-", "’": "'", "‘": "'",
         "“": '"', "”": '"', "·": "*", "…": "..."}


def entities(s: str) -> str:
    return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in s)


def convert_html(src: str) -> str:
    out, pos = [], 0
    for m in SCRIPT.finditer(src):
        out.append(entities(src[pos:m.start()]))
        out.append(m.group(1) + "\n"
                   + json.dumps(json.loads(m.group(2)), indent=2, ensure_ascii=True)
                   + "\n" + m.group(3))
        pos = m.end()
    out.append(entities(src[pos:]))
    return "".join(out)


def convert_plain(src: str) -> str:
    for a, b in PLAIN.items():
        src = src.replace(a, b)
    return src


def meaning(src: str):
    """Karşılaştırılabilir anlam: entity'ler çözülmüş HTML + ayrıştırılmış JSON."""
    parts, pos = [], 0
    for m in SCRIPT.finditer(src):
        parts.append(html.unescape(src[pos:m.start()]))
        parts.append(json.dumps(json.loads(m.group(2)), sort_keys=True))
        pos = m.end()
    parts.append(html.unescape(src[pos:]))
    return parts


def main() -> None:
    root = pathlib.Path(__file__).parent
    targets = [pathlib.Path(a) for a in sys.argv[1:]] or \
              sorted(root.rglob("*.html")) + [root / "llms.txt"]

    for f in targets:
        src = f.read_text(encoding="utf-8")
        if all(ord(c) < 128 for c in src):
            print(f"{f.name:<24} zaten ASCII")
            continue

        if f.suffix == ".html":
            new = convert_html(src)
            if meaning(src) != meaning(new):
                print(f"{f.name:<24} ATLANDI - anlam değişiyor")
                continue
        else:
            new = convert_plain(src)

        assert all(ord(c) < 128 for c in new), f"{f}: hâlâ ASCII dışı karakter var"
        f.write_text(new, encoding="utf-8")
        print(f"{f.name:<24} çevrildi ({len(src)} -> {len(new)} bayt)")


if __name__ == "__main__":
    main()
