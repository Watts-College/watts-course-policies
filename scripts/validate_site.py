"""Check built local links and the legacy redirect; optionally compare a cleanup build."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

SITE_ROOT = "https://watts-college.github.io/watts-course-policies/"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.references = []
        self.refresh = []
        self.canonical = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.references.append(attrs[name])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh.append(attrs.get("content", ""))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))


def validate(root, baseline=None):
    root = root.resolve()
    parsed = {}
    for path in root.rglob("*.html"):
        page = Page(path.read_text(encoding="utf-8"))
        assert len(page.ids) == len(set(page.ids)), f"Duplicate IDs: {path}"
        parsed[path] = page

    index = root / "index.html"
    assert index in parsed, "The policies page was not built"
    for path, page in parsed.items():
        location = urljoin(SITE_ROOT, path.relative_to(root).as_posix())
        for reference in page.references:
            url = urlsplit(urljoin(location, reference))
            if url.scheme not in ("http", "https") or url.netloc != urlsplit(SITE_ROOT).netloc:
                continue
            assert url.path.startswith(urlsplit(SITE_ROOT).path), f"Link leaves site base path: {reference}"
            relative = unquote(url.path[len(urlsplit(SITE_ROOT).path):])
            target = (root / relative).resolve()
            assert target.is_relative_to(root), f"Link escapes build directory: {reference}"
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Missing local target: {path}: {reference}"
            if url.fragment and target in parsed:
                assert unquote(url.fragment) in parsed[target].ids, f"Missing anchor: {path}: {reference}"

    redirect_path = root / "review" / "index.html"
    assert redirect_path in parsed, "The /review/ redirect was not built"
    redirect = parsed[redirect_path]
    assert redirect.canonical == [SITE_ROOT], "Unexpected redirect canonical URL"
    assert any(value == "0; url=/watts-course-policies/" for value in redirect.refresh), "Missing redirect refresh fallback"
    assert "/watts-course-policies/" in redirect.references, "Missing redirect fallback link"

    if baseline:
        baseline = baseline.resolve()
        assert index.read_bytes() == (baseline / "index.html").read_bytes(), "Rendered policies HTML changed during cleanup"
        for relative in (
            "assets/css/policies.css",
            "assets/icons/favicon-32x32.png",
            "assets/posts/ASU_WattsPublicService_3_Horiz_RGB_Black_600ppi.png",
        ):
            assert (root / relative).read_bytes() == (baseline / relative).read_bytes(), f"Retained asset changed: {relative}"
        print("Rendered policies HTML, stylesheet, logo, and favicon match the pre-cleanup build.")
    print(f"Validated local references in {len(parsed)} HTML pages and the /review/ redirect.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    validate(args.site, args.baseline)
