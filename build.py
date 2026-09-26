#!/usr/bin/env python3
"""Builds the site in every language from the templates.

    python3 build.py

template.html + texts.py            → index.html and <lang>/index.html
template-privacy.html + privacy.py  → datenschutz-app/<lang>/index.html (the app's privacy policy)

English is the primary language and lives at the root; every other language gets its
own folder. A new language = one more entry in LANGUAGES and one more dictionary in
each texts file. impressum/ and datenschutz/ (the website's own legal pages) are
static and not built here.
"""
import re
from pathlib import Path

from texts import T
from privacy import P

HERE = Path(__file__).parent
SITE = "https://hybrid-autopress.com/"

# code, folder, name in its own language, hreflang
LANGUAGES = [
    ("en", "", "English", "en"),
    ("de", "de/", "Deutsch", "de"),
    ("fr", "fr/", "Français", "fr"),
    ("es", "es/", "Español", "es"),
    ("it", "it/", "Italiano", "it"),
    ("pt", "pt/", "Português", "pt"),
    ("nl", "nl/", "Nederlands", "nl"),
    ("ja", "ja/", "日本語", "ja"),
    ("zh", "zh/", "简体中文", "zh-Hans"),
]


def render(template, values, target):
    def fill(match):
        key = match.group(1)
        if key not in values:
            raise KeyError(f"{target.relative_to(HERE)} asks for {key!r}, which {values['lang']} does not have")
        return values[key]

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(re.sub(r"\{\{(\w+)\}\}", fill, template), encoding="utf-8")
    print("wrote", target.relative_to(HERE))


def hreflangs(prefix, folders):
    lines = [f'<link rel="alternate" hreflang="{hl}" href="{SITE}{prefix}{folders[c]}">' for c, _, _, hl in LANGUAGES]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{prefix}{folders["en"]}">')
    return "\n".join(lines)


def menu(root, folders, current):
    items = []
    for c, _, n, hl in LANGUAGES:
        current_mark = ' aria-current="page"' if c == current else ""
        items.append(f'<li><a href="{root}{folders[c]}" hreflang="{hl}" lang="{c}"{current_mark}>{n}</a></li>')
    return "".join(items)


PAGE_FOLDERS = {c: p for c, p, _, _ in LANGUAGES}
PRIVACY_FOLDERS = {c: f"datenschutz-app/{c}/" for c, _, _, _ in LANGUAGES}


def build_page(code, path, name):
    root = "../" * path.count("/")
    values = dict(T[code], lang=code, root=root, site=SITE, canonical=SITE + path, lang_name=name,
                  lang_menu=menu(root, PAGE_FOLDERS, code), lang_list=menu(root, PAGE_FOLDERS, code),
                  hreflangs=hreflangs("", PAGE_FOLDERS))
    render((HERE / "template.html").read_text(encoding="utf-8"), values, HERE / path / "index.html")


def build_privacy(code, path, name):
    root = "../../"
    values = dict(P[code], lang=code, root=root, site=SITE, canonical=SITE + PRIVACY_FOLDERS[code], lang_name=name,
                  lang_menu=menu(root, PRIVACY_FOLDERS, code), home=root + path, hreflangs=hreflangs("", PRIVACY_FOLDERS))
    render((HERE / "template-privacy.html").read_text(encoding="utf-8"), values, HERE / PRIVACY_FOLDERS[code] / "index.html")


def build_sitemap():
    urls = [SITE + p for _, p, _, _ in LANGUAGES] + [SITE + PRIVACY_FOLDERS[c] for c, _, _, _ in LANGUAGES]
    urls += [SITE + "impressum/", SITE + "datenschutz/"]
    body = "\n".join("  <url><loc>" + u + "</loc></url>" for u in urls)
    head = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    (HERE / "sitemap.xml").write_text(head + body + "\n</urlset>\n", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    for code, path, name, _ in LANGUAGES:
        if code in T:
            build_page(code, path, name)
        else:
            print("no page texts for", code)
    for code, path, name, _ in LANGUAGES:
        if code in P:
            build_privacy(code, path, name)
        else:
            print("no privacy texts for", code)
    build_sitemap()
