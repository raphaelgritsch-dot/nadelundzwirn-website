import os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import cv2

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
os.makedirs('qr2', exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')

# ---------- QR-Matrix aus der vorhandenen SVG lesen ----------
svg = open('../qr-nadelundzwirn.svg', encoding='utf-8').read()
d = re.search(r' d="([^"]+)"', svg).group(1)
toks = re.findall(r'[MmHh]|-?\d+\.?\d*', d)
cells = set(); x = y = 0; i = 0
while i < len(toks):
    c = toks[i]; i += 1
    if c == 'M':
        x = float(toks[i]); y = float(toks[i + 1]); i += 2
    elif c == 'm':
        x += float(toks[i]); y += float(toks[i + 1]); i += 2
    elif c == 'h':
        l = float(toks[i]); i += 1
        for k in range(int(round(l))):
            cells.add((int(round(x)) + k, int(y)))
        x += l
N = 29
FZ = [(0, 0), (22, 0), (0, 22)]


def in_finder(a, b):
    return any(fx - 1 <= a <= fx + 7 and fy - 1 <= b <= fy + 7 for fx, fy in FZ)


DARK = '#0a0a0a'; RED = '#c9282c'; CREAM = '#f3f2ee'


def qr_svg(shape='round', mod=DARK, eye='round', ring=DARK, core=RED, tile=CREAM, rx=2.4, q=2):
    S = N + 2 * q
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">' % (S, S)]
    if tile:
        o.append('<rect width="%d" height="%d" rx="%s" fill="%s"/>' % (S, S, rx, tile))
    data = sorted(c for c in cells if not in_finder(*c))
    if shape in ('sq', 'round', 'dot', 'diamond'):
        for a, b in data:
            px, py = a + q, b + q
            if shape == 'sq':
                o.append('<rect x="%s" y="%s" width="1.04" height="1.04" fill="%s"/>' % (px - .02, py - .02, mod))
            elif shape == 'round':
                o.append('<rect x="%.2f" y="%.2f" width="0.94" height="0.94" rx="0.36" fill="%s"/>' % (px + .03, py + .03, mod))
            elif shape == 'dot':
                o.append('<circle cx="%.2f" cy="%.2f" r="0.5" fill="%s"/>' % (px + .5, py + .5, mod))
            else:
                o.append('<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="%s"/>' % (px + .5, py - .12, px + 1.12, py + .5, px + .5, py + 1.12, px - .12, py + .5, mod))
    elif shape == 'vbar':
        for a in range(N):
            b = 0
            while b < N:
                if (a, b) in cells and not in_finder(a, b):
                    e = b
                    while e + 1 < N and (a, e + 1) in cells and not in_finder(a, e + 1):
                        e += 1
                    o.append('<rect x="%.2f" y="%.2f" width="0.92" height="%.2f" rx="0.42" fill="%s"/>' % (a + q + .04, b + q + .03, e - b + 0.94, mod))
                    b = e + 1
                else:
                    b += 1
    elif shape == 'hbar':
        for b in range(N):
            a = 0
            while a < N:
                if (a, b) in cells and not in_finder(a, b):
                    e = a
                    while e + 1 < N and (e + 1, b) in cells and not in_finder(e + 1, b):
                        e += 1
                    o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="0.92" rx="0.42" fill="%s"/>' % (a + q + .03, b + q + .04, e - a + 0.94, mod))
                    a = e + 1
                else:
                    a += 1
    for fx, fy in FZ:
        X0, Y0 = fx + q, fy + q
        if eye == 'round':
            o.append('<rect x="%s" y="%s" width="6" height="6" rx="1.7" fill="none" stroke="%s" stroke-width="1"/>' % (X0 + .5, Y0 + .5, ring))
            o.append('<rect x="%s" y="%s" width="3" height="3" rx="0.9" fill="%s"/>' % (X0 + 2, Y0 + 2, core))
        elif eye == 'dot':
            o.append('<circle cx="%s" cy="%s" r="3" fill="none" stroke="%s" stroke-width="1"/>' % (X0 + 3.5, Y0 + 3.5, ring))
            o.append('<circle cx="%s" cy="%s" r="1.7" fill="%s"/>' % (X0 + 3.5, Y0 + 3.5, core))
        else:
            o.append('<rect x="%s" y="%s" width="7" height="7" fill="%s"/>' % (X0, Y0, ring))
            o.append('<rect x="%s" y="%s" width="5" height="5" fill="%s"/>' % (X0 + 1, Y0 + 1, tile or CREAM))
            o.append('<rect x="%s" y="%s" width="3" height="3" fill="%s"/>' % (X0 + 2, Y0 + 2, core))
    o.append('</svg>')
    return '\n'.join(o)


def save_svg(n, **kw):
    f = 'qr2/q%02d.svg' % n
    open(f, 'w', encoding='utf-8').write(qr_svg(**kw))
    return 'qr2/q%02d.svg' % n


# ---------- Karte ----------
PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 3a2 2 0 0 1-.5 2.1L8 10.1a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c1 .3 2 .5 3 .7a2 2 0 0 1 1.6 2z"/></svg>'
ML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 6l10 7 10-7"/></svg>'
GL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 0 0 0 0 20"/></svg>'
PN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
ITEMS = [(PH, '+43 677 61817640'), (ML, 'office@nadelundzwirn.at'), (GL, 'www.nadelundzwirn.at'), (PN, 'Klagenfurt, Kärnten')]

BASE = """
  @page{ size: 89mm 59mm; margin: 0; }
  *{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body{ margin: 0; padding: 0; }
  body{ width: 89mm; height: 59mm; }
  :root{ --bg:#0a0a0a; --ink:#f3f2ee; --dim:#a7a6a1; --red:#c9282c; }
  :root{ --disp:'Archivo Black','Inter',Arial,sans-serif; --body:'Inter',Arial,sans-serif; }
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
  .qx{ position:absolute; display:block; }
  .qx img{ width:100%; height:100%; display:block; }
"""
CORN = {'tl': '<i class="c tl"></i>', 'tr': '<i class="c tr"></i>', 'bl': '<i class="c bl"></i>', 'br': '<i class="c br"></i>'}


def corners(skip=()):
    return ''.join(v for k, v in CORN.items() if k not in skip)


def text(left=34, top=8.5, rows_top=21.5):
    r = ''.join('<div class="row"><span class="ic">%s</span>%s</div>' % (i, t) for i, t in ITEMS)
    return ('<p class="abs name" style="left:%smm;top:%smm">Raphael Gritsch</p>'
            '<p class="abs role caps" style="left:%smm;top:%smm">Gründer</p>'
            '<div class="abs" style="left:%smm;top:%smm">%s</div>') % (left, top, left, top + 5.2, left, rows_top, r)


def card(n, css, body):
    html = ('<!DOCTYPE html>\n<html lang="de"><head><meta charset="UTF-8"><title>QR %02d</title>\n'
            '<link href="../../../fonts/fonts.css" rel="stylesheet">\n<style>%s%s</style></head>\n'
            '<body><div class="page"><div class="t">%s</div></div></body></html>\n') % (n, BASE, css, body)
    open('qr2/k%02d.html' % n, 'w', encoding='utf-8').write(html)


def im(n, style, extra=''):
    return '<div class="qx" style="%s"%s><img src="q%02d.svg" alt="QR"></div>' % (style, extra, n)


POS = 'left:9.3mm;top:50%;transform:translateY(-50%);width:20mm;height:20mm;'

# 01 eckig, creme Kachel, schwarz
save_svg(1, shape='sq', eye='sq', ring=DARK, core=DARK, rx=0.0)
card(1, '', corners() + im(1, POS) + text())
# 02 eckig mit roten Augen, abgerundete Kachel
save_svg(2, shape='sq', eye='sq', ring=DARK, core=RED, rx=2.4)
card(2, '', corners() + im(2, POS) + text())
# 03 Punkte, runde Augen mit roter Mitte
save_svg(3, shape='dot', eye='dot', ring=DARK, core=RED)
card(3, '', corners() + im(3, POS) + text())
# 04 rote Module, schwarze Augen
save_svg(4, shape='round', mod=RED, eye='round', ring=DARK, core=DARK)
card(4, '', corners() + im(4, POS) + text())
# 05 komplett rot auf Creme
save_svg(5, shape='round', mod=RED, eye='round', ring=RED, core=RED)
card(5, '', corners() + im(5, POS) + text())
# 06 senkrechte Balken
save_svg(6, shape='vbar', eye='round', ring=DARK, core=RED)
card(6, '', corners() + im(6, POS) + text())
# 07 waagrechte Balken (Fadenoptik)
save_svg(7, shape='hbar', eye='round', ring=DARK, core=RED)
card(7, '', corners() + im(7, POS) + text())
# 08 Rauten
save_svg(8, shape='diamond', eye='sq', ring=DARK, core=RED, rx=2.4)
card(8, '', corners() + im(8, POS) + text())
# 09 roter Rand um die Kachel
save_svg(9, shape='round', eye='round', ring=DARK, core=RED)
card(9, '.qx{ border-radius:2.4mm; } ', corners() + im(9, POS + 'outline:.4mm solid #c9282c;outline-offset:.9mm;border-radius:1.5mm;') + text())
# 10 Kamerasucher-Winkel um die Kachel
save_svg(10, shape='round', eye='round', ring=DARK, core=RED)
sf = ('<div class="qx" style="left:6.3mm;top:50%;transform:translateY(-50%);width:26mm;height:26mm;">'
      '<i class="c" style="left:0;top:0;width:3.4mm;height:3.4mm;border-top-width:.4mm;border-left-width:.4mm"></i>'
      '<i class="c" style="right:0;top:0;width:3.4mm;height:3.4mm;border-top-width:.4mm;border-right-width:.4mm"></i>'
      '<i class="c" style="left:0;bottom:0;width:3.4mm;height:3.4mm;border-bottom-width:.4mm;border-left-width:.4mm"></i>'
      '<i class="c" style="right:0;bottom:0;width:3.4mm;height:3.4mm;border-bottom-width:.4mm;border-right-width:.4mm"></i></div>')
card(10, '', corners() + sf + im(10, POS.replace('width:20mm;height:20mm', 'width:19mm;height:19mm').replace('9.3mm', '9.8mm')) + text())
# 11 runde Scheibe
save_svg(11, shape='round', eye='round', ring=DARK, core=RED, tile=None, q=1)
circle = '<div class="qx" style="left:8.3mm;top:50%;transform:translateY(-50%);width:22mm;height:22mm;border-radius:50%;background:#f3f2ee;"></div>'
card(11, '', corners() + circle + im(11, 'left:12.3mm;top:50%;transform:translateY(-50%);width:14mm;height:14mm;') + text())
# 12 feine rote Linie im Kachelinneren
save_svg(12, shape='round', eye='round', ring=DARK, core=RED)
inner = '<div class="qx" style="left:9.9mm;top:50%;transform:translateY(-50%);width:18.8mm;height:18.8mm;border:.22mm solid #c9282c;border-radius:1.6mm;pointer-events:none;"></div>'
card(12, '', corners() + im(12, POS) + inner + text())
# 13 Block läuft links aus der Karte
save_svg(13, shape='round', eye='round', ring=DARK, core=RED, tile=None, q=0)
blk = '<div class="qx" style="left:-2mm;top:50%;transform:translateY(-50%);width:29mm;height:25mm;background:#f3f2ee;"></div>'
card(13, '', corners(skip=('tl', 'bl')) + blk + im(13, 'left:4.2mm;top:50%;transform:translateY(-50%);width:19.6mm;height:19.6mm;') + text())
# 14 harter roter Versatzschatten
save_svg(14, shape='round', eye='round', ring=DARK, core=RED)
card(14, '', corners() + im(14, POS + 'filter:drop-shadow(1.1mm 1.1mm 0 #c9282c);') + text())
# 15 Kachel mit Beschriftung unten
save_svg(15, shape='round', eye='round', ring=DARK, core=RED, tile=None, q=1)
cap = ('<div class="qx" style="left:9.3mm;top:50%;transform:translateY(-50%);width:20mm;height:23.6mm;background:#f3f2ee;border-radius:2.4mm;">'
       '<img src="q15.svg" alt="QR" style="position:absolute;left:1.1mm;top:1.1mm;width:17.8mm;height:17.8mm">'
       '<p class="caps" style="position:absolute;left:0;right:0;bottom:2.1mm;text-align:center;font-size:1.45mm;letter-spacing:.3em;color:#0a0a0a;padding-left:.3em">Scannen</p></div>')
card(15, '', corners() + cap + text())
# 16 warmes Sand als Kachelfarbe
save_svg(16, shape='round', eye='round', ring=DARK, core=RED, tile='#e4dccf')
card(16, '', corners() + im(16, POS) + text())
# 17 kühles Hellgrau
save_svg(17, shape='round', eye='round', ring=DARK, core=RED, tile='#d3d3cf')
card(17, '', corners() + im(17, POS) + text())
# 18 groß
save_svg(18, shape='round', eye='round', ring=DARK, core=RED)
card(18, '', corners() + im(18, 'left:7.4mm;top:50%;transform:translateY(-50%);width:23.6mm;height:23.6mm;') + text(left=35))
# 19 oben bündig mit dem Namen, Beschriftung darunter
save_svg(19, shape='round', eye='round', ring=DARK, core=RED)
card(19, '', corners() + im(19, 'left:9.5mm;top:8.2mm;width:19.6mm;height:19.6mm;') +
     '<p class="abs caps" style="left:9.5mm;top:29.6mm;width:19.6mm;text-align:center;font-size:1.5mm;letter-spacing:.3em;color:#a7a6a1;padding-left:.3em">Scannen</p>' + text())
# 20 Eckanker unten rechts, Text links
save_svg(20, shape='round', eye='round', ring=DARK, core=RED)
card(20, '', corners(skip=('br',)) + im(20, 'right:4mm;bottom:4mm;width:19.6mm;height:19.6mm;') + text(left=10))

# ---------- Rendern, Prüfen, Übersicht ----------
E = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
dec = cv2.QRCodeDetector()
res = {}
for n in range(1, 21):
    src = os.path.join(here, 'qr2', 'k%02d.html' % n)
    url = 'file:///' + src.replace('\\', '/').replace(' ', '%20').replace('ä', '%C3%A4')
    for sc, name in ((3, 'k%02d.png' % n), (10, 't%02d.png' % n)):
        subprocess.run([E, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=%d' % sc,
                        '--window-size=337,223', '--virtual-time-budget=3000', '--screenshot=' + os.path.join(here, 'qr2', name), url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    img = cv2.imread(os.path.join(here, 'qr2', 't%02d.png' % n))
    r = dec.detectAndDecode(img)[0]
    res[n] = r
    os.remove(os.path.join(here, 'qr2', 't%02d.png' % n))
    print(n, repr(r))

w, h = Image.open(os.path.join(here, 'qr2', 'k01.png')).size
pad, lab = 36, 80


def sheet(nums, name):
    W = lab + 2 * w + lab + pad
    H = pad + 5 * (h + pad)
    out = Image.new('RGB', (W, H), (92, 92, 92))
    dr = ImageDraw.Draw(out)
    try:
        f = ImageFont.truetype('arialbd.ttf', 46)
    except Exception:
        f = ImageFont.load_default()
    for i, n in enumerate(nums):
        r_, c_ = divmod(i, 2)
        x = lab + c_ * (w + lab + pad)
        y = pad + r_ * (h + pad)
        dr.text((x - lab + 14, y + h // 2 - 24), '%02d' % n, fill=(255, 255, 255), font=f)
        out.paste(Image.open(os.path.join(here, 'qr2', 'k%02d.png' % n)).convert('RGB'), (x, y))
    out.save(os.path.join(here, name))
    print(name, out.size)


sheet(range(1, 11), 'qr2-ideen-1-bis-10.png')
sheet(range(11, 21), 'qr2-ideen-11-bis-20.png')
