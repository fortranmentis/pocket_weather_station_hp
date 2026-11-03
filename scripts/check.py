#!/usr/bin/env python3
"""Check bilingual parity, links, anchors, screenshot assets, and page metadata."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'scripts/content.json').read_text())
assert data['en'].keys() == data['ko'].keys(), 'Locale keys differ'
assert len(data['screens']) == 14
assert len({s['id'] for s in data['screens']}) == 14
assert all('{n}' in data[lang]['screenCount'] for lang in ('en', 'ko'))

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.tags = path, set(), [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.path}: duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        for attr in ('src', 'href'):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        for candidate in attrs.get('srcset', '').split(','):
            if candidate.strip():
                self.links.append(candidate.strip().split()[0])
        if tag == 'img':
            assert 'alt' in attrs, f'{self.path}: image without alt'

homes = (ROOT / 'index.html', ROOT / 'ko/index.html')
documents = tuple(ROOT / lang / page / 'index.html' for lang in ('', 'ko') for page in ('privacy', 'support'))
pages = {path: Page(path) for path in homes + documents}
links = 0
for path, page in pages.items():
    assert sum(tag == 'h1' for tag, _ in page.tags) == 1
    assert sum(tag == 'main' for tag, _ in page.tags) == 1
    if path in homes:
        assert sum(attrs.get('class') == 'gallery-card' for _, attrs in page.tags) == 14
        assert sum(attrs.get('role') == 'tabpanel' for _, attrs in page.tags) == 3
    assert sum(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in page.tags) == 1
    assert sum(tag == 'link' and attrs.get('hreflang') in ('en','ko') for tag, attrs in page.tags) == 2
    for url in page.links:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            assert parts.scheme == 'https', url
            assert 'github.com/fortranmentis/pocket_weather_station/' not in url + '/', f'Private app repository linked: {url}'
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if target.is_relative_to(ROOT) and target.is_dir() and not (target / 'index.html').exists():
            raise AssertionError(f'{path.relative_to(ROOT)}: directory without index.html: {url}')
        if target.is_dir():
            target /= 'index.html'
        assert target.is_relative_to(ROOT), f'Link escapes site root: {url}'
        assert target.exists(), f'{path.relative_to(ROOT)}: missing {url}'
        if parts.fragment and target.suffix == '.html':
            target_page = pages.get(target) or Page(target)
            assert unquote(parts.fragment) in target_page.ids, f'Unknown fragment: {url}'
        links += 1
    for _, attrs in page.tags:
        for attr in ('aria-controls', 'aria-labelledby', 'aria-describedby'):
            for value in attrs.get(attr, '').split():
                assert value in page.ids, f'Missing ARIA target: {value}'

sitemap = (ROOT / 'sitemap.xml').read_text()
for path in pages:
    assert f"<loc>https://fortranmentis.github.io/pocket_weather_station_hp/{path.parent.relative_to(ROOT).as_posix() + '/' if path.parent != ROOT else ''}</loc>" in sitemap, f'Missing from sitemap: {path}'

for screen in data['screens']:
    for suffix in ('', '-600'):
        image = ROOT / f'assets/screenshots/{screen["id"]}{suffix}.jpg'
        assert image.stat().st_size > 1000
assert (ROOT / 'assets/social-preview.jpg').stat().st_size > 1000
assert (ROOT / '.nojekyll').exists()
print(f'PASS: 2 languages, 2 home pages with 28 gallery entries and 6 app panels, 4 privacy/support pages, sitemap, {links} local asset/link references, 28 screenshot files, ARIA references and SEO metadata.')
