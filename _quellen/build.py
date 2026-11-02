#!/usr/bin/env python3
"""Baut den Onepager aus _quellen/template.html in den Repo-Root.

Aufruf aus dem Repo-Root:  python3 _quellen/build.py

Ergebnis:
  index.html    öffentlich – nur echte Städte, Zusagen ab 0, keine Platzhalter
  entwurf.html  für das Team – alle Beispieldaten und Platzhalter, gelbe Leiste, noindex
  img/, fonts/  werden aus _quellen/ kopiert

Was bearbeitest du wo? (alles in _quellen/template.html)
  - Texte und Abschnitte: direkt im HTML
  - Städte: Liste `var C=[ ... ]` im Script. Eine Stadt erscheint öffentlich nur mit `echt:1`.
    tp (Treffpunkt) und c (Zusagen) sind Beispieldaten und werden öffentlich geleert bzw. auf 0 gesetzt.
  - Nur im Entwurf: Block zwischen <!--entwurf--> und <!--/entwurf-->
  - Material: <!--mat:material/DATEI-->…<!--/mat--> erscheint öffentlich erst, wenn die Datei im Repo liegt
  - Platzhalter-Markierungen: <span class="ph">…</span> – öffentlich automatisch entfernt
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SITE = 'https://leon-xnexusdev.github.io/wsz-onepage/'   # bei eigener Domain ändern (auch og:url/og:image im Template)
IMG = {'LOGO': 'logo.webp', 'CROWD1': 'demo-verdi.jpg', 'CROWD2': 'demo-blockade.jpg'}


def fmt(n):
    return f'{n:,}'.replace(',', '.')


def render(tpl, draft):
    t = tpl
    a = t.index('  var C=['); z = t.index('];', a)
    lines = t[a:z].split('\n')
    if not draft:
        lines = [l for l in lines if not l.strip().startswith('{n:') or 'echt:1' in l]
        lines = [re.sub(r",c:\d+", ",c:0", re.sub(r"tp:'[^']*'", "tp:''", l)) for l in lines]
    data = '\n'.join(lines)
    t = t[:a] + data + t[z:]
    total = sum(int(x) for x in re.findall(r",c:(\d+),side:", data))
    t = t.replace('{{TOTAL}}', fmt(total)).replace('{{TOTAL_HIDDEN}}', '' if total else ' hidden')
    if draft:
        t = re.sub(r'<!--/?(entwurf|matsec|mat:[^>]*)-->', '', t).replace('<!--/mat-->', '')
        return t
    t = re.sub(r'<!--entwurf-->.*?<!--/entwurf-->', '', t, flags=re.S)
    t = re.sub(r'<!--mat:([^>]*)-->(.*?)<!--/mat-->',
               lambda m: m.group(2) if os.path.exists(os.path.join(REPO, m.group(1))) else '', t, flags=re.S)
    if '<article class="mat">' not in t[t.index('<!--matsec-->'):t.index('<!--/matsec-->')]:
        t = re.sub(r'<!--matsec-->.*?<!--/matsec-->', '', t, flags=re.S)
        t = t.replace(" Material gibt's weiter unten.", '')
    t = t.replace('<!--matsec-->', '').replace('<!--/matsec-->', '')
    t = re.sub(r'<span class="ph(?:\s[^"]*)?"[^>]*>[^<]*</span>', '', t)
    t = re.sub(r"'<span class=\"ph(?:\s[^\"]*)?\">[^<]*</span>'", "''", t)
    t = re.sub(r"        if\(DRAFT\)h\+=.*?';\n", '', t, flags=re.S)
    t = t.replace('/* Städte. Treffpunkte und Zahlen sind Beispieldaten. */', '/* Städte */')
    assert 'class="ph ' not in t and 'class="ph"' not in t, 'Platzhalter in der öffentlichen Fassung übrig'
    return t


def wrap(t, draft):
    i = t.index('</style>') + 8
    head = t[:i]
    if draft:
        head = head.replace('<meta name="theme-color" content="#26326b">',
                            '<meta name="theme-color" content="#26326b">\n<meta name="robots" content="noindex, nofollow">')
        head = head.replace(f'<meta property="og:url" content="{SITE}">', f'<meta property="og:url" content="{SITE}entwurf.html">')
    bar = ('<aside class="draftbar" aria-label="Hinweis">Entwurf für das Team: Platzhalter und Beispieldaten sind sichtbar. '
           '<a href="index.html">Öffentliche Version</a></aside>\n') if draft else ''
    body = t[i:].replace('Zum Inhalt springen</a>\n', 'Zum Inhalt springen</a>\n' + bar, 1)
    out = ('<!doctype html>\n<html lang="de"' + (' data-entwurf' if draft else '') + '>\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    return out.replace('body{overflow-x:clip;background:var(--bg);', 'body{margin:0;overflow-x:clip;background:var(--bg);')


def assets(t):
    for sub in ('img', 'fonts'):
        os.makedirs(os.path.join(REPO, sub), exist_ok=True)
        for fn in os.listdir(os.path.join(ROOT, sub)):
            shutil.copy(os.path.join(ROOT, sub, fn), os.path.join(REPO, sub, fn))
    for k, name in IMG.items():
        t = t.replace('{{%s}}' % k, f'img/{name}')
    return re.sub(r'\{\{FONT_([a-z-]+)_(\d+)\}\}', r'fonts/\1-latin-\2-normal.woff2', t)


def build():
    tpl = open(os.path.join(ROOT, 'template.html')).read()
    for fn, draft in (('index.html', False), ('entwurf.html', True)):
        open(os.path.join(REPO, fn), 'w').write(wrap(assets(render(tpl, draft)), draft))
    n = len(re.findall(r"\{n:'[^']*',echt:1", tpl))
    print(f'ok – index.html (öffentlich, {n} echte Städte) und entwurf.html gebaut')


if __name__ == '__main__':
    build()
