"""Convert an H5P Course Presentation (.h5p) into a reveal.js deck.

Usage: python3 h5p2reveal.py LECTURE.h5p OUTPUT_DIR [NAME.html]
Writes OUTPUT_DIR/NAME.html (default index.html) and copies images to OUTPUT_DIR/images/.
"""
import json, html, sys, os, zipfile
src, outdir = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
c = json.loads(z.read('content/content.json'))
meta = json.loads(z.read('h5p.json'))
for name in z.namelist():
    if name.startswith('content/') and not name.endswith('/') and name != 'content/content.json':
        dest = os.path.join(outdir, name[len('content/'):])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(z.read(name))
out = os.path.join(outdir, sys.argv[3] if len(sys.argv) > 3 else 'index.html')
slides = c['presentation']['slides']

def box(e, extra=''):
    return (f'left:{e["x"]:.3f}%;top:{e["y"]:.3f}%;'
            f'width:{e["width"]:.3f}%;height:{e["height"]:.3f}%;{extra}')

def element(e):
    a = e['action']; lib = a['library'].split(' ')[0]; p = a['params']
    if lib == 'H5P.AdvancedText':
        return f'<div class="el text" style="{box(e)}">{p["text"]}</div>'
    if lib == 'H5P.Table':
        return f'<div class="el text table" style="{box(e)}">{p["text"]}</div>'
    if lib == 'H5P.Image':
        alt = html.escape(p.get('alt') or p.get('title') or '', quote=True)
        return (f'<div class="el img" style="{box(e)}">'
                f'<img src="{p["file"]["path"]}" alt="{alt}"></div>')
    if lib == 'H5P.Shape':
        if p['type'] in ('horizontal-line', 'vertical-line'):
            l = p['line']; side = 'top' if p['type'] == 'horizontal-line' else 'left'
            w = int(l['borderWidth']) / 16  # px at 640-wide base -> em
            return (f'<div class="el shape {p["type"]}" style="{box(e)}">'
                    f'<div style="border-{side}:{w}em {l["borderStyle"]} {l["borderColor"]}"></div></div>')
        s = p['shape']
        radius = '50%' if p['type'] == 'circle' else f'{int(s.get("borderRadius", 0)) / 16}em'
        return (f'<div class="el" style="{box(e)}background:{s["fillColor"]};'
                f'border:{int(s["borderWidth"]) / 16}em {s["borderStyle"]} {s["borderColor"]};'
                f'border-radius:{radius}"></div>')
    if lib == 'H5P.Link':
        w = p['linkWidget']; url = w['protocol'] + w['url']
        return (f'<div class="el text link" style="{box(e)}">'
                f'<a href="{html.escape(url, quote=True)}" target="_blank">{p.get("title") or url}</a></div>')
    raise ValueError(lib)

parts = []
for sl in slides:
    bg = sl.get('slideBackgroundSelector', {}).get('fillSlideBackground')
    kw = ', '.join(k['main'].strip() for k in sl.get('keywords', []))
    attrs = (f' data-background-color="{bg}"' if bg else '') + \
            (f' data-keywords="{html.escape(kw, quote=True)}"' if kw else '')
    body = '\n'.join(element(e) for e in sl['elements'])
    notes = '\n'.join(e['solution'] for e in sl['elements'] if e.get('solution'))
    if notes:
        body += f'\n<aside class="notes">{notes}</aside>'
    parts.append(f'<section{attrs}>\n{body}\n</section>')

title = html.escape(meta.get('title', 'Presentation'))
page = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<style>
  /* Slide = 1280x720; base font scaled to match H5P text metrics */
  .reveal {{ font-size: 24px; font-family: "Open Sans", Arial, sans-serif; color: #000; }}
  .reveal .slides section {{ position: absolute; width: 100%; height: 100%; padding: 0; text-align: left; }}
  .reveal .el {{ position: absolute; box-sizing: border-box; overflow: visible; }}
  .reveal .el.text {{ padding: .375em .5em; line-height: 1.25; }}
  .reveal .el.text p, .reveal .el.text li {{ margin: 0 0 .5em 0; line-height: 1.25; }}
  .reveal .el.text ul {{ display: block; margin: 0 0 .5em 1.25em; padding: 0; }}
  .reveal .el.text h3 {{ font-size: 1em; text-transform: none; margin: 0 0 .5em; color: #000; font-family: inherit; }}
  .reveal .el.img img {{ width: 100%; height: 100%; object-fit: contain; margin: 0; max-width: none; max-height: none; }}
  .reveal .el.shape {{ display: flex; flex-direction: column; justify-content: center; }}
  .reveal .el.vertical-line {{ flex-direction: row; justify-content: center; }}
  .reveal .el.vertical-line > div {{ height: 100%; }}
  .reveal .el.link {{ display: flex; align-items: center; justify-content: center; font-size: 1.5em; }}
  .reveal .el.table table {{ margin: 0 auto; border-collapse: collapse; font-size: 1em; }}
  .reveal .el.table td {{ border: 1px solid #555; padding: .3em .5em; vertical-align: top; }}
  .reveal a {{ color: #1a73d9; }}
</style>
</head>
<body>
<div class="reveal">
<div class="slides">
{chr(10).join(parts)}
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
<script>
  Reveal.initialize({{
    width: 1280, height: 720, margin: 0.02,
    center: false, hash: true, slideNumber: 'c/t',
    transition: 'slide',
    plugins: [RevealNotes]
  }});
</script>
</body>
</html>
'''
open(out, 'w', encoding='utf-8').write(page)
print(len(parts), 'slides')
