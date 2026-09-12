#!/usr/bin/env python3
"""Her sayfa icin 1200x630 OG gorseli uret.

Paylasilan bir baglanti gorselsizse Reddit, Slack ve X'te ciplak bir satir
olarak cikiyor. Sayfa zaten Reddit'te dolasiyor, yani bu dogrudan tiklama
kaybi.

Yerlesim ve palet marketing/ads/reddit/build.py ile ayni kaynaktan: reklam,
site ve uygulama gozle ayni urun gorunsun.

    python3 og.py
"""
from __future__ import annotations
import pathlib, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = pathlib.Path(__file__).parent

# (cikti adi, ust satir, buyuk baslik, alt satir)
CARDS = [
    ("og", "Thyrowise", "A thyroid tracker that keeps<br><em>everything on your phone</em>.",
     "TSH, levothyroxine and symptoms &#183; free on iPhone"),
    ("og-levothyroxine-coffee-timing", "Levothyroxine timing",
     "Coffee: <em>an hour</em>.<br>Food: 30 to 60 minutes.",
     "Every number on the page names its source"),
    ("og-what-is-a-normal-tsh", "Reference ranges",
     "What is a <em>normal TSH</em>,<br>and why labs disagree.",
     "About 0.4 to 4.0 mIU/L &#8212; and why that is not the whole answer"),
    ("og-hashimotos-symptom-tracking", "Symptom tracking",
     "Arrive with a <em>pattern</em>,<br>not a feeling.",
     "What to log for Hashimoto's, and what not to bother with"),
    ("og-best-thyroid-tracker-apps", "Choosing an app",
     "Seven things that<br><em>actually matter</em>.",
     "Including what Thyrowise does not do"),
    ("og-faq", "Thyrowise", "No account.<br><em>No server.</em>",
     "Pricing, privacy, Android, Apple Watch &#8212; answered"),
    ("og-support", "Sources", "Every medical sentence<br><em>names its source</em>.",
     "ATA &#183; NIDDK &#183; MedlinePlus &#183; ACR"),
]

CSS = """
:root{--bg:#F7F5FC;--accent:#6B529E;--plum:#946187;--text:#26242E;--soft:#706B7D;--sep:#E0DBE8}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:var(--bg);color:var(--text);overflow:hidden;
  font-family:-apple-system,"SF Pro Display","Inter",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;display:flex;flex-direction:column;padding:64px 72px}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:auto}
.brand span{font-size:26px;font-weight:600;letter-spacing:-.2px}
.kicker{font-size:19px;font-weight:600;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--soft);margin-bottom:20px}
h1{font-size:72px;line-height:1.08;font-weight:700;letter-spacing:-2px}
h1 em{font-style:normal;color:var(--accent)}
.foot{margin-top:auto;padding-top:30px;border-top:1px solid var(--sep);
  display:flex;justify-content:space-between;align-items:baseline;
  font-size:22px;color:var(--soft)}
.foot b{color:var(--accent);font-weight:600}
"""

MARK = """<svg width="44" height="44" viewBox="0 0 108 108">
<g transform="translate(54,52) scale(0.42)">
<g transform="translate(-36,-12) rotate(28)"><ellipse rx="37" ry="29" fill="#6B529E" fill-opacity=".5"/></g>
<g transform="translate(36,-12) rotate(-28)"><ellipse rx="37" ry="29" fill="#6B529E" fill-opacity=".5"/></g>
<g transform="translate(-28,26) rotate(-20)"><ellipse rx="26" ry="21" fill="#946187" fill-opacity=".65"/></g>
<g transform="translate(28,26) rotate(20)"><ellipse rx="26" ry="21" fill="#946187" fill-opacity=".65"/></g>
<rect x="-6" y="-32" width="12" height="64" rx="6" fill="#6B529E"/>
</g></svg>"""


def render(stem: str, kicker: str, title: str, foot: str) -> None:
    doc = f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style>
<div class="brand">{MARK}<span>Thyrowise</span></div>
<div class="kicker">{kicker}</div>
<h1>{title}</h1>
<div class="foot"><span>thyrowise.github.io</span><b>{foot}</b></div>"""
    # build.py ile ayni desen: CWD'ye yaz, goreli adlarla cagir.
    src = ROOT / f"_{stem}.html"
    src.write_text(doc, encoding="utf-8")
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1200,630",
                        f"--screenshot={stem}.png", src.name],
                       check=True, capture_output=True, cwd=ROOT)
    finally:
        src.unlink(missing_ok=True)
    print(f"  {stem}.png  {(ROOT / (stem + '.png')).stat().st_size // 1024} KB")


def main() -> None:
    if not pathlib.Path(CHROME).exists():
        sys.exit("Chrome bulunamadi: " + CHROME)
    for card in CARDS:
        render(*card)


if __name__ == "__main__":
    main()
