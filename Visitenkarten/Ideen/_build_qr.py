import os, re, subprocess
from PIL import Image, ImageDraw, ImageFont

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 3a2 2 0 0 1-.5 2.1L8 10.1a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c1 .3 2 .5 3 .7a2 2 0 0 1 1.6 2z"/></svg>'
ML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 6l10 7 10-7"/></svg>'
GL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 0 0 0 0 20"/></svg>'
PN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
ITEMS = [(PH, '+43 677 61817640'), (ML, 'office@nadelundzwirn.at'), (GL, 'www.nadelundzwirn.at'), (PN, 'Klagenfurt, Kärnten')]
X = '✕'

# QR-Varianten: hell (für schwarzen Grund) und rot
svg = open('../qr-nadelundzwirn.svg', encoding='utf-8').read()
open('qr-hell.svg', 'w', encoding='utf-8').write(svg.replace('#1a1512', '#f3f2ee'))
open('qr-rot.svg', 'w', encoding='utf-8').write(svg.replace('#1a1512', '#c9282c'))
QR = '<img src="../qr-nadelundzwirn.svg" alt="QR">'

BASE = """
  @page{ size: 89mm 59mm; margin: 0; }
  *{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body{ margin: 0; padding: 0; }
  body{ width: 89mm; height: 59mm; }
  :root{ --bg:#0a0a0a; --ink:#f3f2ee; --dim:#a7a6a1; --faint:#6c6c67; --red:#c9282c; --line:#2b2b2b;
    --disp:'Archivo Black','Inter',Arial,sans-serif; --body:'Inter',Arial,sans-serif; }
  p{ margin: 0; }
  .page{ position: relative; width: 89mm; height: 59mm; overflow: hidden; background: var(--bg); color: var(--ink); font-family: var(--body); }
  .t{ position: absolute; left: 2mm; top: 2mm; width: 85mm; height: 55mm; }
  .abs{ position: absolute; }
  .caps{ font-weight: 700; text-transform: uppercase; }
  .c{ position:absolute; width:5mm; height:5mm; border:0 solid var(--red); }
  .tl{ left:4mm; top:4mm; border-top-width:.45mm; border-left-width:.45mm; }
  .tr{ right:4mm; top:4mm; border-top-width:.45mm; border-right-width:.45mm; }
  .bl{ left:4mm; bottom:4mm; border-bottom-width:.45mm; border-left-width:.45mm; }
  .br{ right:4mm; bottom:4mm; border-bottom-width:.45mm; border-right-width:.45mm; }
  .name{ font-family:var(--disp); text-transform:uppercase; font-size:4mm; line-height:1; white-space:nowrap; }
  .role{ font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
  .row{ display:flex; align-items:center; height:5.5mm; font-size:2.5mm; white-space:nowrap; }
  .ic{ width:4.6mm; height:4.6mm; border:.3mm solid var(--red); border-radius:50%; color:var(--red); display:flex; align-items:center; justify-content:center; margin-right:2.6mm; flex:none; }
  .ic svg{ width:2.3mm; height:2.3mm; }
  .qr{ position:absolute; background:#fff; padding:1.15mm; }
  .qr img, .qrp img{ width:100%; height:100%; display:block; }
  .qrp{ position:absolute; }
"""
CORNERS = {'tl': '<i class="c tl"></i>', 'tr': '<i class="c tr"></i>', 'bl': '<i class="c bl"></i>', 'br': '<i class="c br"></i>'}


def corners(skip=()):
    return ''.join(v for k, v in CORNERS.items() if k not in skip)


def rows(items=ITEMS, cls='abs rows', style=''):
    return '<div class="%s" style="%s">%s</div>' % (cls, style, ''.join('<div class="row"><span class="ic">%s</span>%s</div>' % (i, t) for i, t in items))


def head(left, top=8.5, align=''):
    return ('<p class="abs name" style="left:%smm;top:%smm;%s">Raphael Gritsch</p>'
            '<p class="abs role caps" style="left:%smm;top:%smm;%s">Gründer</p>') % (left, top, align, left, top + 5.2, align)


def doc(n, css, body):
    html = ('<!DOCTYPE html>\n<html lang="de"><head><meta charset="UTF-8"><title>QR-Idee %02d</title>\n'
            '<link href="../../fonts/fonts.css" rel="stylesheet">\n<style>%s%s</style></head>\n'
            '<body><div class="page"><div class="t">%s</div></div></body></html>\n') % (n, BASE, css, body)
    open('qr-%02d.html' % n, 'w', encoding='utf-8').write(html)


# 01 Scan-Rahmen: rote Winkel um den QR-Code wie ein Kamerasucher
css = """
 .sf{ position:absolute; left:6.5mm; top:50%; transform:translateY(-50%); width:24mm; height:24mm; }
 .sf i{ position:absolute; width:3.4mm; height:3.4mm; border:0 solid var(--red); }
 .sf .a{ left:0; top:0; border-top-width:.4mm; border-left-width:.4mm; } .sf .b{ right:0; top:0; border-top-width:.4mm; border-right-width:.4mm; }
 .sf .c2{ left:0; bottom:0; border-bottom-width:.4mm; border-left-width:.4mm; } .sf .d{ right:0; bottom:0; border-bottom-width:.4mm; border-right-width:.4mm; }
"""
body = (corners() + '<div class="sf"><i class="a"></i><i class="b"></i><i class="c2"></i><i class="d"></i></div>'
        '<div class="qr" style="left:10.2mm;top:50%;transform:translateY(-50%);width:17.2mm;height:17.2mm">' + QR + '</div>'
        + head(34) + rows(style='left:34mm;top:21.5mm'))
doc(1, css, body)

# 02 Spiegelbild: Text links, QR rechts
body = (corners() + head(10) + rows(style='left:10mm;top:21.5mm')
        + '<div class="qr" style="right:10mm;top:50%;transform:translateY(-50%);width:20mm;height:20mm">' + QR + '</div>')
doc(2, '', body)

# 03 Eckanker: QR sitzt dort, wo sonst der Eckwinkel unten rechts steht
body = (corners(skip=('br',)) + head(10) + rows(style='left:10mm;top:21.5mm')
        + '<div class="qr" style="right:4mm;bottom:4mm;width:19mm;height:19mm">' + QR + '</div>')
doc(3, '', body)

# 04 Invertiert: helle Module direkt auf Schwarz, ohne weiße Fläche
body = (corners() + head(10) + rows(style='left:10mm;top:21.5mm')
        + '<div class="qrp" style="right:10mm;top:50%;transform:translateY(-50%);width:20mm;height:20mm"><img src="qr-hell.svg" alt="QR"></div>')
doc(4, '', body)

# 05 Rot gedruckt: weiße Fläche, rote Module
body = (corners() + head(10) + rows(style='left:10mm;top:21.5mm')
        + '<div class="qr" style="right:10mm;top:50%;transform:translateY(-50%);width:20mm;height:20mm"><img src="qr-rot.svg" alt="QR"></div>')
doc(5, '', body)

# 06 Beschriftet: QR links mit senkrechter Zeile am Rand
css = """
 .cap{ position:absolute; left:29.6mm; top:50%; transform:translateY(-50%) rotate(180deg); writing-mode:vertical-rl; font-size:1.45mm; letter-spacing:.3em; color:var(--dim); white-space:nowrap; }
 .cap b{ color:var(--red); font-weight:400; margin:1.2mm 0; }
"""
body = (corners() + '<div class="qr" style="left:9mm;top:50%;transform:translateY(-50%);width:19.5mm;height:19.5mm">' + QR + '</div>'
        '<p class="cap caps">Scannen <b>' + X + '</b> Anfragen</p>' + head(34.5) + rows(style='left:34.5mm;top:21.5mm'))
doc(6, css, body)

# 07 Hängendes Etikett: QR als weißes Schild, das oben aus der Kante hängt, alles zentriert
css = """
 .tag{ position:absolute; left:50%; top:-2mm; transform:translateX(-50%); width:21.4mm; height:23mm; background:#fff; padding:2mm 2.4mm 2.4mm; }
 .tag img{ width:16.6mm; height:16.6mm; display:block; margin-top:2mm; }
 .ctr{ position:absolute; left:0; right:0; text-align:center; }
 .grid{ position:absolute; left:8mm; right:8mm; top:36.2mm; display:grid; grid-template-columns:1fr 1fr; column-gap:4mm; }
 .grid .row{ height:5mm; font-size:2.2mm; } .grid .ic{ width:4mm; height:4mm; margin-right:2mm; } .grid .ic svg{ width:2mm; height:2mm; }
"""
g = ''.join('<div class="row"><span class="ic">%s</span>%s</div>' % (i, t) for i, t in [ITEMS[0], ITEMS[2], ITEMS[1], ITEMS[3]])
body = (corners() + '<div class="tag">' + QR + '</div>'
        '<p class="ctr name" style="top:25.4mm;font-size:3.7mm">Raphael Gritsch</p><p class="ctr role caps" style="top:30.2mm">Gründer</p>'
        '<div class="grid">' + g + '</div>')
doc(7, css, body)

# 08 Kante rechts: weißer Block läuft aus dem Rand, der QR-Code sitzt darin
css = """
 .blk{ position:absolute; right:-2mm; top:50%; transform:translateY(-50%); width:27mm; height:25mm; background:#fff; }
 .blk img{ position:absolute; left:3mm; top:2.5mm; width:20mm; height:20mm; }
"""
body = (corners(skip=('tr', 'br')) + head(10) + rows(style='left:10mm;top:21.5mm') + '<div class="blk">' + QR + '</div>')
doc(8, css, body)

# 09 Tafel: leicht aufgehelltes Feld links, QR-Code darin, rote Kante
css = """
 .panel{ position:absolute; left:-2mm; top:-2mm; bottom:-2mm; width:31mm; background:#141414; border-right:.4mm solid var(--red); }
"""
body = ('<div class="panel"></div>' + corners() + '<div class="qr" style="left:4.5mm;top:50%;transform:translateY(-50%);width:19.5mm;height:19.5mm">' + QR + '</div>'
        + head(34) + rows(style='left:34mm;top:21.5mm'))
doc(9, css, body)

# 10 Faden: rote Linie läuft vom Text direkt in den QR-Code
css = """
 .thread{ position:absolute; left:10mm; width:48mm; top:21.4mm; border-top:.5mm solid var(--red); }
"""
body = (corners() + head(10, 8.5) + '<div class="thread"></div>' + rows(style='left:10mm;top:24.4mm')
        + '<div class="qr" style="right:10mm;top:21.4mm;transform:translateY(-50%);width:18.5mm;height:18.5mm">' + QR + '</div>')
doc(10, css, body)

# ---------- Rendern ----------
E = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for n in range(1, 11):
    src = os.path.join(here, 'qr-%02d.html' % n)
    out = os.path.join(here, 'qr-%02d.png' % n)
    url = 'file:///' + src.replace('\\', '/').replace(' ', '%20').replace('ä', '%C3%A4')
    subprocess.run([E, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=3',
                    '--window-size=337,223', '--virtual-time-budget=3000', '--screenshot=' + out, url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ims = [Image.open(os.path.join(here, 'qr-%02d.png' % n)).convert('RGB') for n in range(1, 11)]
w, h = ims[0].size
pad = 36
lab = 80
cols = 2
rows_n = 5
W = lab + cols * w + (cols) * pad + lab
H = pad + rows_n * (h + pad)
sheet = Image.new('RGB', (W, H), (92, 92, 92))
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype('arialbd.ttf', 46)
except Exception:
    f = ImageFont.load_default()
for i, im in enumerate(ims):
    r, c = divmod(i, 2)
    x = lab + c * (w + pad + lab) if c == 0 else lab + w + pad + lab
    x = lab + c * (w + lab + pad)
    y = pad + r * (h + pad)
    d.text((x - lab + 14, y + h // 2 - 24), '%02d' % (i + 1), fill=(255, 255, 255), font=f)
    sheet.paste(im, (x, y))
sheet.save(os.path.join(here, 'qr-ideen.png'))
print(sheet.size)
