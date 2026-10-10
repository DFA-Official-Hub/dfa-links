#!/usr/bin/env python3
"""Prerender links.json into index.html (no-JS fallback). Run after editing links.json."""
import json, html, re, pathlib
root = pathlib.Path(__file__).parent
links = json.loads((root/'links.json').read_text())
icons = json.loads((root/'assets/icons.json').read_text())
e = lambda s: html.escape(str(s), quote=True)
out = []
for l in links:
    url = (l.get('url') or '').strip()
    if not url:
        continue
    ext = '' if url.startswith('mailto:') else ' target="_blank" rel="noopener"'
    note = ''
    if l.get('note'):
        rows = []
        for x in l['note'].split('\n'):
            a, _, b = x.partition(' – ')
            rows.append(f'<li>{e(a)}' + (f'<b>{e(b)}</b>' if b else '') + '</li>')
        note = '<ul class="note">' + ''.join(rows) + '</ul>'
    feat = ' feat' if l.get('note') else ''
    out.append(f'<li><a class="btn{feat}" data-id="{e(l["id"])}" href="{e(url)}"{ext}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{e(icons.get(l["icon"], ""))}"/></svg><span class="lbl">{e(l["label"])}</span><span class="arr">›</span>{note}</a></li>')
p = root/'index.html'
h = p.read_text()
h = re.sub(r'<!-- PRERENDER:START -->.*?<!-- PRERENDER:END -->',
           lambda m: '<!-- PRERENDER:START -->\n' + '\n'.join(out) + '\n<!-- PRERENDER:END -->', h, flags=re.S)
p.write_text(h)
print(f'{len(out)} visible / {len(links)-len(out)} hidden')
