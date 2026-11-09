#!/usr/bin/env python3
"""Build index.html from src/index.template.html.

Inlines the vendored libraries and the font, then writes a strict Content Security Policy
with SHA-256 hashes of the inline <style> and <script> blocks, so the page can run nothing
but its own code and makes no network requests.

Usage:  python3 build.py           (writes index.html)
        python3 build.py --check   (exits 1 if index.html is out of date)
Needs only the Python 3 standard library.
"""
import base64, hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent

def read(p):
    return (ROOT / p).read_text(encoding="utf-8")

def build():
    html = read("src/index.template.html")
    font = base64.b64encode((ROOT / "fonts/InstrumentSans-latin.woff2").read_bytes()).decode()
    parts = [("Cellwork", "LICENSE"),
             ("d3-delaunay 6.0.4", "licenses/d3-delaunay.txt"),
             ("Delaunator 5 (bundled in d3-delaunay)", "licenses/delaunator.txt"),
             ("robust-predicates 3 (bundled in d3-delaunay)", "licenses/robust-predicates.txt"),
             ("Clipper JS 6.4.2", "licenses/clipper-BSL-1.0.txt"),
             ("JSBN (bundled in Clipper JS)", "licenses/jsbn.txt"),
             ("Instrument Sans font", "licenses/instrument-sans-OFL.txt")]
    licences = "\n\n".join(f"===== {name} =====\n\n{read(path).strip()}" for name, path in parts)
    if "</script" in licences.lower():
        sys.exit("build: licence text must not contain </script")
    for marker, value in (("/*LICENSES*/", licences),
                          ("/*FONTDATA*/", font),
                          ("/*D3DELAUNAY*/", read("vendor/d3-delaunay.min.js")),
                          ("/*CLIPPER*/", read("vendor/clipper.min.js"))):
        if html.count(marker) != 1:
            sys.exit(f"build: expected exactly one {marker} in the template")
        html = html.replace(marker, value)

    def hashes(tag):
        blocks = re.findall(rf"<{tag}>(.*?)</{tag}>", html, flags=re.S)
        if not blocks:
            sys.exit(f"build: no <{tag}> blocks found")
        return " ".join("'sha256-%s'" % base64.b64encode(hashlib.sha256(b.encode()).digest()).decode() for b in blocks)

    csp = ("default-src 'none'; "
           f"script-src {hashes('script')}; "
           f"style-src {hashes('style')}; "
           "img-src blob: data:; font-src data:; connect-src 'none'; media-src 'none'; "
           "object-src 'none'; frame-src 'none'; worker-src 'none'; manifest-src 'none'; "
           "base-uri 'none'; form-action 'none'")
    if html.count("<!--CSP-->") != 1:
        sys.exit("build: expected exactly one <!--CSP--> marker")
    return html.replace("<!--CSP-->", f'<meta http-equiv="Content-Security-Policy" content="{csp}">')

if __name__ == "__main__":
    out = build()
    target = ROOT / "index.html"
    if "--check" in sys.argv:
        ok = target.exists() and target.read_text(encoding="utf-8") == out
        print("index.html is up to date" if ok else "index.html is out of date: run python3 build.py")
        sys.exit(0 if ok else 1)
    target.write_text(out, encoding="utf-8")
    print(f"wrote index.html ({len(out.encode()) // 1024} KB)")
