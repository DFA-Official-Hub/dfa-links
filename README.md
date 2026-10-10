# DFA Links – Deutsch Für Alle link-in-bio page

Static page: `index.html` + `links.json` + `assets/`.

## How to fill links.json

`links.json` is an array; each entry becomes one button, **in the same order**:

```json
{ "id": "udemy", "label": "Udemy Course", "url": "", "icon": "courses", "note": "optional" }
```

| Field | Meaning |
|---|---|
| `id` | unique short name (no spaces) |
| `label` | button text |
| `url` | link (`https://…`, `mailto:…`, `https://wa.me/…?text=…`). **Empty `""` = button hidden.** |
| `icon` | key from `assets/icons.json` (instagram, threads, tiktok, youtube, facebook, pinterest, linkedin, spotify, apple-podcasts, amazon-music, whatsapp, email, courses, book, shop, globe, classroom, newsletter). To add one, add `"name": "<SVG path d for a 24x24 viewBox>"` to icons.json. |
| `note` | optional; lines separated by `\n`, shown under the button. `Name – Price` lines put the price on the right (fee list). |

To show a hidden button (e.g. Free A1 Workbook, Gumroad, Udemy, Etsy, Amazon KDP, Website, Google Classroom, Newsletter, Amazon Music), paste its URL into `url`.
WhatsApp prefilled text must be URL-encoded (`python3 -c "import urllib.parse;print(urllib.parse.quote('your text'))"`).

After editing, run:

```sh
python3 build.py
```

This prerenders the buttons into `index.html` so the page works without JavaScript. With JS, the page also re-reads `links.json` live (needs http(s), not `file://`).

Local preview: `python3 -m http.server 8000` → http://localhost:8000
