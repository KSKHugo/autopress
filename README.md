# Hybrid AutoPress — website

The one-page site for [Hybrid AutoPress](https://kskhugo.github.io/autopress/), the app that
uploads many Markdown files to WordPress at once — for iPhone, iPad and Mac.

Live: <https://kskhugo.github.io/autopress/> (English) · <https://kskhugo.github.io/autopress/de/> (Deutsch)

## How it is built

Plain HTML, CSS and a little JavaScript — no framework, no dependencies, served by GitHub Pages
straight from `main`.

```
template.html      the structure of the page, with {{placeholders}}
build.py           the words, per language; writes index.html and de/index.html
assets/style.css   design: navy #1A3A5E / #254E7A and amber #F59E0B from the app icon
assets/site.js     reveal on scroll, the pinned walkthrough, the hero zoom
assets/img/        app icon and screenshots (Mac, iPad, iPhone)
impressum/         the legal notice (German law), a static page in the same design
serve.js           tiny static server for a local preview: node serve.js
```

Change words in `build.py`, structure in `template.html`, then:

```bash
python3 build.py
```

`index.html` and `de/index.html` are generated — do not edit them by hand. A further language is
one more dictionary in `build.py`.

## The scroll

Every section is a full-height panel and a resting point (`scroll-snap`, proximity). In
“How it works” the Mac window stays pinned while four steps scroll past and swap the screenshot.
On small screens and with “reduce motion” the page falls back to a plain, linear scroll.

## Screenshots

| Mac | iPad | iPhone |
|---|---|---|
| ![Mac](assets/img/mac-main.png) | ![iPad](assets/img/ipad-main.jpg) | ![iPhone](assets/img/iphone-done.jpg) |

Taken from debug builds of the app with its demo launch arguments (`-demoFolder`, `-demoSite`,
`-demoSelect`, `-demoUpload`) against the mock WordPress from the app repository. The content
(“Coastline Journal”) is sample content; the pictures in it are drawn by a script.

© 2026 Pascal Hugo
