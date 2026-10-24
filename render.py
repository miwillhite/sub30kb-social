"""Render SubThirtyKB posts in posts.json to PNGs under out/<post id>/.

Usage: python3 render.py [--from YYYY-MM-DD] [--to YYYY-MM-DD]
"""
import argparse, json, pathlib
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
SIZES = {"card": (1080, 1350), "carousel": (1080, 1350), "sub10": (1080, 1080),
         "cue": (1080, 1080), "mantra": (1080, 1080)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="frm"); ap.add_argument("--to")
    a = ap.parse_args()
    posts = json.loads((ROOT / "posts.json").read_text())
    posts = [p for p in posts if (not a.frm or p["date"] >= a.frm) and (not a.to or p["date"] <= a.to)]
    env = Environment(loader=FileSystemLoader(ROOT / "templates"))
    fonts = (ROOT / "node_modules/@fontsource").as_uri()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in posts:
            w, h = SIZES[p["type"]]
            out = ROOT / "out" / p["id"]; out.mkdir(parents=True, exist_ok=True)
            slides = range(len(p["moves"]) + 2) if p["type"] == "carousel" else [None]
            pg = b.new_page(viewport={"width": w, "height": h})
            for s in slides:
                html = env.get_template(p["type"] + ".html").render(p=p, slide=s, fonts=fonts)
                f = out / "tmp.html"; f.write_text(html)
                pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
                name = f"{s+1:02d}.png" if s is not None else "01.png"
                pg.screenshot(path=str(out / name), clip={"x": 0, "y": 0, "width": w, "height": h})
            f.unlink(); pg.close()
            (out / "caption.txt").write_text(p["caption"])
            print("rendered", p["id"])
        b.close()

if __name__ == "__main__":
    main()
