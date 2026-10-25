#!/usr/bin/env python3
"""Prerender links.json into index.html (no-JS fallback). Run after editing links.json."""
import json, html, re, pathlib
root = pathlib.Path(__file__).parent
links = json.loads((root/'links.json').read_text())
icons = json.loads((root/'assets/icons.json').read_text())
e = lambda s: html.escape(str(s), quote=True)
out = []
for l in links:
    if l.get('children'):
        kids = [c for c in l['children'] if (c.get('url') or '').strip()]
        if not kids:
            continue
        rows = ''.join(f'<li><a href="{e(c["url"].strip())}" target="_blank" rel="noopener">{e(c["label"])}</a></li>' for c in kids)
        out.append(f'<li><details class="group" data-id="{e(l["id"])}"><summary class="btn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{e(icons.get(l["icon"], ""))}"/></svg><span class="lbl">{e(l["label"])}</span><span class="arr">›</span></summary><ul class="sublinks">{rows}</ul></details></li>')
        continue
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
    gc = f' data-goatcounter-click="{e(l["click"])}" data-goatcounter-title="{e(l.get("clickTitle", l["label"]))}"' if l.get('click') else ''
    out.append(f'<li><a class="btn{feat}" data-id="{e(l["id"])}" href="{e(url)}"{ext}{gc}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{e(icons.get(l["icon"], ""))}"/></svg><span class="lbl">{e(l["label"])}</span><span class="arr">›</span>{note}</a></li>')
p = root/'index.html'
h = p.read_text()
h = re.sub(r'<!-- PRERENDER:START -->.*?<!-- PRERENDER:END -->',
           lambda m: '<!-- PRERENDER:START -->\n' + '\n'.join(out) + '\n<!-- PRERENDER:END -->', h, flags=re.S)
p.write_text(h)
print(f'{len(out)} visible / {len(links)-len(out)} hidden')
