"""Generate static, script-free localized Weekline legal pages."""
from pathlib import Path
import json
from html import escape as e

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text())
BASE = 'https://nextlinecode.github.io/nextlinecode-Legal/Weekline/'
REFS = [('Google Privacy Policy', 'https://policies.google.com/privacy'), ('Firebase Privacy and Security', 'https://firebase.google.com/support/privacy'), ('Google Analytics Data Retention', 'https://support.google.com/analytics/answer/7667196'), ('Apple Privacy Policy', 'https://www.apple.com/legal/privacy/'), ('GitHub Privacy Statement', 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'), ('Apple Standard EULA', 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/')]

def shell(lang, title, body, path, prefix, alternates=''):
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Weekline</title><meta name="description" content="{e(title)} — Weekline by nextlinecode">
<link rel="canonical" href="{BASE}{path}">{alternates}<link rel="stylesheet" href="{prefix}styles.css"></head>
<body><header><a class="brand" href="{prefix}index.html">WEEKLINE<span></span></a></header><main>{body}</main>
<footer><p>nextlinecode · <a href="mailto:nextlinecode@gmail.com">nextlinecode@gmail.com</a></p><p>© 2026 nextlinecode</p></footer></body></html>'''

def document(lang, kind, alias=False):
    d = DATA[lang]
    prefix = '' if alias else '../'
    nav = '<nav aria-label="Languages">' + ''.join(f'<a href="{prefix}{code}/{kind}.html" hreflang="{code}" lang="{code}"'+ (' aria-current="page"' if code == lang else '') + f'>{e(v["label"])}</a>' for code,v in DATA.items()) + '</nav>'
    body = nav + f'<h1>{e(d[kind+"Title"])}</h1><p class="date">{e(d["date"])}</p><p>{e(d[kind+"Intro"])}</p>'
    for section in d[kind]:
        body += '<section><h2>'+e(section[0])+'</h2>' + ''.join('<p>'+e(p)+'</p>' for p in section[1:]) + '</section>'
    other = 'terms' if kind == 'privacy' else 'privacy'
    body += '<aside><p><a href="'+(lang+'/' if alias else '')+other+'.html">'+e(d[other+'Title'])+'</a></p><ul>'+''.join(f'<li><a href="{url}">{e(label)}</a></li>' for label,url in REFS)+'</ul></aside>'
    alts = ''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}{code}/{kind}.html">' for code in DATA)
    return shell(lang,d[kind+'Title'],body,f'{lang}/{kind}.html',prefix,alts)

for lang in DATA:
    (ROOT/lang).mkdir(exist_ok=True)
    for kind in ('privacy','terms'):
        (ROOT/lang/(kind+'.html')).write_text(document(lang,kind))
for kind in ('privacy','terms'):
    (ROOT/(kind+'.html')).write_text(document('en',kind,True))
body = '<h1>Legal information</h1><p>개인정보처리방침 · 이용약관</p><div class="languages">'
for lang,d in DATA.items():
    body += f'<section lang="{lang}"><h2>{e(d["label"])}</h2><p><a href="{lang}/privacy.html">{e(d["privacyTitle"])}</a></p><p><a href="{lang}/terms.html">{e(d["termsTitle"])}</a></p></section>'
body += '</div><p><a href="../index.html">Nextlinecode Legal</a></p>'
(ROOT/'index.html').write_text(shell('en','Legal information',body,'index.html',''))
