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

pages = {path: Page(path) for path in (ROOT / 'index.html', ROOT / 'ko/index.html')}
links = 0
for path, page in pages.items():
    assert sum(tag == 'h1' for tag, _ in page.tags) == 1
    assert sum(tag == 'main' for tag, _ in page.tags) == 1
    assert sum(attrs.get('class') == 'gallery-card' for _, attrs in page.tags) == 14
    assert sum(attrs.get('role') == 'tabpanel' for _, attrs in page.tags) == 3
    assert sum(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in page.tags) == 1
    assert sum(tag == 'link' and attrs.get('hreflang') in ('en','ko') for tag, attrs in page.tags) == 2
    for url in page.links:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            assert parts.scheme == 'https', url
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
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

for screen in data['screens']:
    for suffix in ('', '-600'):
        image = ROOT / f'assets/screenshots/{screen["id"]}{suffix}.jpg'
        assert image.stat().st_size > 1000
assert (ROOT / 'assets/social-preview.jpg').stat().st_size > 1000
assert (ROOT / '.nojekyll').exists()
print(f'PASS: 2 languages, 28 gallery entries, 6 app panels, {links} local asset/link references, 28 screenshot files, ARIA references and SEO metadata.')
