"""Static unfurl / association checks; these do not claim live messenger approval."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlparse
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
JOIN = ROOT / "panchigi/join"
CANONICAL = "https://baekwangho.github.io/panchigi/join/"

class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = []
        self.links = []
        self.title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta": self.meta.append(attrs)
        if tag == "link": self.links.append(attrs)
        if tag == "title": self.title = True

head = Head()
head.feed((JOIN / "index.html").read_text(encoding="utf-8"))
def values(key):
    return [m["content"] for m in head.meta if m.get("property", m.get("name")) == key]
for key in ("description", "og:title", "og:description", "og:image", "og:image:width", "og:image:height",
            "og:image:alt", "og:url", "og:type", "og:locale", "og:site_name", "twitter:card",
            "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"):
    assert values(key) and all(values(key)), key
assert head.title
assert values("og:url") == [CANONICAL]
assert values("og:locale") == ["ko_KR"]
assert values("og:site_name") == ["판치기"]
assert values("og:type") == ["website"]
assert values("twitter:card") == ["summary_large_image"]
assert len(values("og:image")) == 2
image_results = []
for src, width, height, alt in zip(values("og:image"), values("og:image:width"), values("og:image:height"), values("og:image:alt")):
    url = urlparse(src)
    assert url.scheme == "https" and url.netloc == "baekwangho.github.io" and not url.query
    path = ROOT / url.path.lstrip("/")
    with Image.open(path) as image:
        assert image.format == "PNG" and image.size == (int(width), int(height))
    assert path.stat().st_size < 300_000
    image_results.append({"path": path.relative_to(ROOT).as_posix(), "width": int(width), "height": int(height),
                          "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
assert (image_results[0]["width"], image_results[0]["height"]) == (1200, 630)
assert (image_results[1]["width"], image_results[1]["height"]) == (600, 600)
# Meta recommends 1200x630. X allows at least 300x157, up to 4096px, PNG <5MB.
# A square alternative helps cropping clients; the chosen card remains platform-specific.
assert values("twitter:image") == values("og:image")[:1]
for rel in ("canonical", "icon", "apple-touch-icon"):
    entry = next(link for link in head.links if link.get("rel") == rel)
    if rel == "canonical": assert entry["href"] == CANONICAL
    else: assert (JOIN / entry["href"]).is_file()
assert Image.open(JOIN / "assets/apple-touch-icon.png").size == (180, 180)
assert (ROOT / ".nojekyll").exists()
android = json.loads((ROOT / ".well-known/assetlinks.json").read_text())
pan = next(e for e in android if e["target"].get("package_name") == "com.panchigi")
assert pan["target"]["namespace"] == "android_app"
assert "delegate_permission/common.handle_all_urls" in pan["relation"]
assert all(re.fullmatch(r"(?:[A-F0-9]{2}:){31}[A-F0-9]{2}", x) for x in pan["target"]["sha256_cert_fingerprints"])
apple = json.loads((ROOT / ".well-known/apple-app-site-association").read_text())
pan = next(e for e in apple["applinks"]["details"] if e.get("appID") == "XF5CMG6QGW.com.panchigi")
assert pan["paths"] == ["/panchigi/join/*"]
print(json.dumps({"staticChecks": "PASS", "images": image_results,
                  "liveUnfurls": "pending publication approval", "playAppSigningSha256": "TODO Play Console"}, ensure_ascii=False, indent=2))
