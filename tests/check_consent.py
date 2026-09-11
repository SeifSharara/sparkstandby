"""Dependency-free checks for the public demo and consent contract."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.links=[]; self.tags=[]; self.ids=set()
        self.source=path.read_text(); self.feed(self.source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append(tag)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag=='a': self.links.append(attrs.get('href', ''))

pages={route:Page(ROOT / route / 'index.html') for route in ['', 'demo', 'demo/ready', 'privacy', 'terms', 'sms-consent']}
for route,p in pages.items():
    for old in ['857-837-6539','857) 837-6539','18578376539','only SMS opt-in method','only opt-in method','phone IVR','press 1','ivr-verbal-consent-evidence.png']:
        assert old not in p.source, (route, old)
    for link in p.links:
        if link.startswith('/'):
            target=ROOT / link.split('#')[0].lstrip('/')
            assert target.exists(), (route,link)
for route in ['demo','demo/ready','sms-consent']:
    p=pages[route]
    assert '(571) 556-5051' in p.source
    assert '/privacy/' in p.links and '/terms/' in p.links
    if route != 'demo':
        assert 'not yet available' in p.source.lower()
    assert 'Seif Sharara' in p.source
assert '/demo/' in pages[''].links and '/demo/' in pages['sms-consent'].links
assert 'tel:+15715565051' in pages['demo/ready'].links
assert 'noindex' in pages['demo/ready'].source
assert not any(t in pages['demo'].tags for t in ['form','input'])
assert pages['demo'].tags.count('iframe') == 1
assert 'https://api.leadconnectorhq.com/widget/form/5WP9sjNGRUWmi2fYcQGk' in pages['demo'].source
assert 'https://link.msgsndr.com/js/form_embed.js' in pages['demo'].source
assert 'not yet available' not in pages['demo'].source.lower()
assert 'Demo form not connected yet' not in pages['demo'].source
assert 'form' not in pages['demo/ready'].tags
assert 'highlevel-form-container' in pages['demo'].ids
for p in pages.values():
    assert 'localStorage' not in p.source and 'sessionStorage' not in p.source
for route in ['privacy','terms']:
    assert 'sole proprietor' in pages[route].source
    assert 'September 10, 2026' in pages[route].source
config=(ROOT/'js/config.js').read_text()
assert 'ivrPhone' not in config and 'ivrStatus' not in config
assert '+15715565051' in config and '+17036781815' in config
assert '<loc>/demo/</loc>' in (ROOT/'sitemap.xml').read_text()
assert '/demo/ready/' not in (ROOT/'sitemap.xml').read_text()
print('PASS: Six routes, consent/identity/number contract, legal links, HighLevel embed, and sitemap.')
