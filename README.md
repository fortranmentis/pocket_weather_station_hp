# Pocket Weather Station · Website

The bilingual product website for **Pocket Weather Station / 기상대**, published with GitHub Pages.

- [English](https://fortranmentis.github.io/pocket_weather_station_hp/)
- [한국어](https://fortranmentis.github.io/pocket_weather_station_hp/ko/)
- Privacy policy: [English](https://fortranmentis.github.io/pocket_weather_station_hp/privacy/) · [한국어](https://fortranmentis.github.io/pocket_weather_station_hp/ko/privacy/)
- Support: [English](https://fortranmentis.github.io/pocket_weather_station_hp/support/) · [한국어](https://fortranmentis.github.io/pocket_weather_station_hp/ko/support/)

An Apple-inspired presentation with large typography, open space, a muted LCD-green palette, and actual app screenshots. Includes the three-view app tour, LCD display, pressure-flow map, widgets and device integration, forecast explanation, a filtered 14-screen gallery with keyboard-accessible magnification, data handling, and FAQs, plus privacy policy and support pages for the App Store listing. This is an independent project, without Apple affiliation.

## Develop

No npm dependencies or runtime framework. The generated HTML is committed, so GitHub Pages can serve the repository root directly.

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/app.js
python3 -m http.server 4173 --bind 127.0.0.1
```

Open `http://localhost:4173/` or `http://localhost:4173/ko/`.

Edit `scripts/content.json` for both languages, then regenerate with `scripts/build.py`; it writes the home, privacy, and support pages and `sitemap.xml`. Shared presentation and interactions live in `assets/style.css` and `assets/app.js`. All local links work beneath the GitHub Pages project path. Change `BASE` in the generator and `robots.txt` if the domain or repository path changes. Crawlers read only the domain-root `robots.txt`, so submit `sitemap.xml` in Search Console or list it in the user site's `robots.txt`.

## Publication

GitHub Pages source: **main branch → / (root)**. `.nojekyll` preserves the plain static site. Push the reviewed HTML, assets, and sources to `main` to update the site. The website repository is separate from the native app repository, which is private; `check.py` fails if a page links to it.

## Content and imagery

Copy was checked against the app README and project settings at app revision `cfc10680f52db7566c1e9a20aca38054d79b8761` (2026-11-03). Source project version: `0.1.0`. The site announces an upcoming App Store launch, as requested by the project owner, without a release date or a live download link. It does not imply current store availability or measured forecast improvements.

The 14 supplied English screenshots have full-resolution JPEGs and 600-pixel variants; their labels and example values are preserved. Korean page copy is localized, while the screenshots remain in English. The app icon comes from the current app asset catalog. Website images are copies; native app assets and original screenshots were not modified.

Forecast weights are default blend inputs, not accuracy measurements. Flow/arrival estimates are heuristic. Temperature and humidity are provider values. Optional iCloud sharing is on by default and can transmit rounded location and pressure summaries; detailed local records are not a claim that no data leaves the device. Refer to current app documentation for implementation details and service requirements.
