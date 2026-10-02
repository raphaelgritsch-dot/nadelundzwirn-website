import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
X = '✕'
PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 3a2 2 0 0 1-.5 2.1L8 10.1a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c1 .3 2 .5 3 .7a2 2 0 0 1 1.6 2z"/></svg>'
ML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 6l10 7 10-7"/></svg>'
GL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 0 0 0 0 20"/></svg>'
PN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
TEL = '+43 677 61817640'
MAIL = 'office@nadelundzwirn.at'
WEB = 'www.nadelundzwirn.at'
ORT = 'Klagenfurt, Kärnten'
QR = '<img src="../qr-nadelundzwirn.svg" alt="QR">'

BASE = """
  @page{ size: 89mm 59mm; margin: 0; }
  *{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body{ margin: 0; padding: 0; }
  body{ width: 89mm; height: 59mm; }
  :root{ --bg:#0a0a0a; --ink:#f3f2ee; --dim:#a7a6a1; --faint:#6c6c67; --red:#c9282c; --line:#2b2b2b;
    --disp:'Archivo Black','Inter',Arial,sans-serif; --body:'Inter',Arial,sans-serif; --script:'Yellowtail',cursive; }
  p{ margin: 0; }
  .page{ position: relative; width: 89mm; height: 59mm; overflow: hidden; background: var(--bg); color: var(--ink); font-family: var(--body); }
  .t{ position: absolute; left: 2mm; top: 2mm; width: 85mm; height: 55mm; }
  .frame{ position: absolute; inset: 3.5mm; border: 0.35mm solid var(--red); pointer-events: none; }
  .abs{ position: absolute; }
  .caps{ font-weight: 700; text-transform: uppercase; }
  .qr{ position: absolute; background: #fff; padding: 1.1mm; }
  .qr img{ width: 100%; height: 100%; display: block; }
"""


def doc(title, css, body):
    return ('<!DOCTYPE html>\n<html lang="de"><head><meta charset="UTF-8"><title>%s</title>\n'
            '<link href="../../fonts/fonts.css" rel="stylesheet">\n<style>%s%s</style></head>\n'
            '<body><div class="page">%s</div></body></html>\n') % (title, BASE, css, body)


def save(n, side, html):
    with open('Ideen/idee-%02d-%s.html' % (n, side), 'w', encoding='utf-8') as f:
        f.write(html)


def fix(path, light=False):
    s = open(path, encoding='utf-8').read()
    s = s.replace('../fonts/fonts.css', '../../fonts/fonts.css')
    s = s.replace('src="qr-nadelundzwirn.svg"', 'src="../qr-nadelundzwirn.svg"')
    if light:
        s = s.replace('--bg-0: #0a0a0a;', '--bg-0: #f3f2ee;').replace('--fg: #f3f2ee;', '--fg: #0a0a0a;')
        s = s.replace('--fg-dim: #a7a6a1;', '--fg-dim: #5d5c58;').replace('--line: #2b2b2b;', '--line: #d6d4cd;')
        s = s.replace('background: #fff;', 'background: transparent;')
    return s


def rows_icons(items):
    return ''.join('<div class="row"><span class="ic">%s</span>%s</div>' % (i, t) for i, t in items)


# ---------- 01 Klassisch (aktuell) ----------
save(1, 'v', fix('visitenkarte-2026-vorne.html'))
save(1, 'r', fix('visitenkarte-2026-hinten.html'))

# ---------- 02 Doppelrahmen + Datentabelle ----------
css = """
 .f2{ position:absolute; inset:5.4mm; border:0.2mm solid #2e2e2e; }
 .word{ position:absolute; left:0; right:0; top:50%; transform:translateY(-56%); text-align:center; font-family:var(--script); font-size:11.5mm; line-height:1; }
 .lab{ position:absolute; left:50%; bottom:3.5mm; transform:translate(-50%,50%); background:var(--bg); padding:0 2.6mm; font-size:1.7mm; letter-spacing:.3em; color:var(--dim); white-space:nowrap; line-height:1; }
"""
save(2, 'v', doc('02v', css, '<div class="t"><div class="frame"></div><div class="f2"></div><p class="word">Nadel &amp; Zwirn</p><p class="lab caps">Stickerei aus Klagenfurt</p></div>'))
css = """
 .f2{ position:absolute; inset:5.4mm; border:0.2mm solid #2e2e2e; }
 .name{ left:8mm; top:8mm; font-family:var(--disp); text-transform:uppercase; font-size:4.6mm; line-height:1; }
 .role{ left:8mm; top:13.6mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .rows{ left:8mm; right:8mm; top:26mm; border-top:.25mm solid var(--line); }
 .row{ display:grid; grid-template-columns:14mm 1fr; align-items:center; padding:1.2mm 0; border-bottom:.25mm solid var(--line); }
 .k{ font-size:1.5mm; letter-spacing:.24em; color:var(--faint); }
 .v{ font-size:2.5mm; }
"""
rows = ''.join('<div class="row"><span class="k caps">%s</span><span class="v">%s</span></div>' % (k, v) for k, v in [('Tel', TEL), ('Mail', MAIL), ('Web', WEB), ('Ort', ORT)])
body = ('<div class="t"><div class="frame"></div><div class="f2"></div><p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p>'
        '<div class="qr" style="right:8mm;top:8mm;width:15.5mm;height:15.5mm">%s</div><div class="abs rows">%s</div></div>') % (QR, rows)
save(2, 'r', doc('02r', css, body))

# ---------- 03 Eckwinkel ----------
corner = """
 .c{ position:absolute; width:5mm; height:5mm; border:0 solid var(--red); }
 .tl{ left:4mm; top:4mm; border-top-width:.45mm; border-left-width:.45mm; }
 .tr{ right:4mm; top:4mm; border-top-width:.45mm; border-right-width:.45mm; }
 .bl{ left:4mm; bottom:4mm; border-bottom-width:.45mm; border-left-width:.45mm; }
 .br{ right:4mm; bottom:4mm; border-bottom-width:.45mm; border-right-width:.45mm; }
"""
C = '<i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>'
css = corner + """
 .word{ position:absolute; left:0; right:0; top:50%; transform:translateY(-62%); text-align:center; font-family:var(--script); font-size:12mm; line-height:1; }
 .tag{ position:absolute; left:0; right:0; top:34.5mm; text-align:center; font-size:1.8mm; letter-spacing:.3em; color:var(--dim); }
 .tag b{ color:var(--red); font-weight:400; margin:0 1.4mm; }
"""
save(3, 'v', doc('03v', css, '<div class="t">%s<p class="word">Nadel &amp; Zwirn</p><p class="tag caps">Stickerei <b>%s</b> Klagenfurt</p></div>' % (C, X)))
css = corner + """
 .name{ left:10mm; top:10mm; font-family:var(--disp); text-transform:uppercase; font-size:4.4mm; line-height:1; }
 .role{ left:10mm; top:15.6mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .rows{ left:10mm; top:24mm; }
 .row{ display:flex; align-items:center; height:5mm; font-size:2.5mm; }
 .row b{ color:var(--red); font-weight:400; font-size:2.2mm; width:5mm; }
"""
rows = ''.join('<div class="row"><b>%s</b>%s</div>' % (X, t) for t in [TEL, MAIL, WEB, ORT])
body = ('<div class="t">%s<p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p><div class="abs rows">%s</div>'
        '<div class="qr" style="right:10mm;bottom:10mm;width:17mm;height:17mm">%s</div></div>') % (C, rows, QR)
save(3, 'r', doc('03r', css, body))

# ---------- 04 Fadenlinie ----------
css = """
 .thread{ position:absolute; left:-2mm; right:-2mm; top:27mm; border-top:.5mm solid var(--red); }
 .word{ position:absolute; left:8mm; bottom:29.4mm; font-family:var(--script); font-size:12mm; line-height:1; }
 .tag{ position:absolute; right:8mm; top:30.5mm; font-size:1.8mm; letter-spacing:.3em; color:var(--dim); }
"""
save(4, 'v', doc('04v', css, '<div class="t"><div class="thread"></div><p class="word">Nadel &amp; Zwirn</p><p class="tag caps">Stickerei aus Klagenfurt</p></div>'))
css = """
 .thread{ position:absolute; left:-2mm; right:-2mm; top:21mm; border-top:.5mm solid var(--red); }
 .name{ left:8mm; top:8mm; font-family:var(--disp); text-transform:uppercase; font-size:4.6mm; line-height:1; }
 .role{ left:8mm; top:14.3mm; font-size:1.8mm; letter-spacing:.24em; color:var(--dim); }
 .rows{ left:8mm; top:25.5mm; font-size:2.5mm; line-height:5.2mm; }
"""
body = ('<div class="t"><div class="thread"></div><p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p>'
        '<div class="abs rows"><p>%s</p><p>%s</p><p>%s</p><p>%s</p></div>'
        '<div class="qr" style="right:8mm;bottom:8mm;width:17mm;height:17mm">%s</div></div>') % (TEL, MAIL, WEB, ORT, QR)
save(4, 'r', doc('04r', css, body))

# ---------- 05 Monogramm ----------
css = """
 .mono{ position:absolute; left:0; right:0; top:13mm; display:flex; justify-content:center; align-items:center; gap:3.4mm; font-family:var(--disp); font-size:19mm; line-height:1; }
 .xx{ position:relative; width:10.5mm; height:10.5mm; }
 .xx::before,.xx::after{ content:''; position:absolute; left:50%; top:50%; width:14.5mm; height:1.7mm; background:var(--red); }
 .xx::before{ transform:translate(-50%,-50%) rotate(45deg); }
 .xx::after{ transform:translate(-50%,-50%) rotate(-45deg); }
 .n1{ position:absolute; left:0; right:0; top:36.5mm; text-align:center; font-size:2.2mm; letter-spacing:.34em; }
 .n2{ position:absolute; left:0; right:0; top:41mm; text-align:center; font-size:1.7mm; letter-spacing:.3em; color:var(--dim); }
"""
save(5, 'v', doc('05v', css, '<div class="t"><div class="frame"></div><div class="mono"><span>N</span><i class="xx"></i><span>Z</span></div><p class="n1 caps">Nadel &amp; Zwirn</p><p class="n2 caps">Stickerei aus Klagenfurt</p></div>'))
save(5, 'r', fix('visitenkarte-2026-hinten.html'))

# ---------- 06 Laufband ----------
band = 'NADEL<i>%s</i>ZWIRN<i>%s</i>NADEL<i>%s</i>ZWIRN' % (X, X, X)
cssb = """
 .band{ position:absolute; left:-6mm; white-space:nowrap; font-family:var(--disp); text-transform:uppercase; font-size:11mm; line-height:1; color:#1d1d1b; letter-spacing:.01em; }
 .band i{ font-style:normal; font-family:var(--body); font-size:6.4mm; color:var(--red); margin:0 3mm; vertical-align:middle; }
"""
css = cssb + """
 .band{ bottom:1.5mm; }
 .word{ position:absolute; left:0; right:0; top:12mm; text-align:center; font-family:var(--script); font-size:12mm; line-height:1; }
 .tag{ position:absolute; left:0; right:0; top:28.4mm; text-align:center; font-size:1.8mm; letter-spacing:.3em; color:var(--dim); }
"""
save(6, 'v', doc('06v', css, '<div class="t"><p class="word">Nadel &amp; Zwirn</p><p class="tag caps">Stickerei aus Klagenfurt</p><div class="band">%s</div></div>' % band))
css = cssb + """
 .band{ top:-4.2mm; }
 .name{ left:9mm; top:13mm; font-family:var(--disp); text-transform:uppercase; font-size:4.4mm; line-height:1; }
 .role{ left:9mm; top:18.6mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .rows{ left:9mm; top:25.5mm; font-size:2.5mm; }
 .row{ display:flex; align-items:center; height:5mm; } .row b{ color:var(--red); font-weight:400; font-size:2mm; width:4.6mm; }
"""
rows = ''.join('<div class="row"><b>%s</b>%s</div>' % (X, t) for t in [TEL, MAIL, WEB, ORT])
body = ('<div class="t"><div class="band">%s</div><p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p><div class="abs rows">%s</div>'
        '<div class="qr" style="right:9mm;bottom:8mm;width:17mm;height:17mm">%s</div></div>') % (band, rows, QR)
save(6, 'r', doc('06r', css, body))

# ---------- 07 Balken ----------
css = """
 .bar{ position:absolute; left:0; top:0; bottom:0; width:8.5mm; background:var(--red); }
 .word{ position:absolute; left:15.5mm; top:19mm; font-family:var(--script); font-size:12mm; line-height:1; }
 .tag{ position:absolute; left:16.2mm; top:34.4mm; font-size:1.8mm; letter-spacing:.3em; color:var(--dim); }
"""
save(7, 'v', doc('07v', css, '<div class="bar"></div><div class="t"><p class="word">Nadel &amp; Zwirn</p><p class="tag caps">Stickerei aus Klagenfurt</p></div>'))
css = """
 .bar{ position:absolute; right:0; top:0; bottom:0; width:8.5mm; background:var(--red); }
 .name{ left:31mm; top:9mm; font-family:var(--disp); text-transform:uppercase; font-size:4mm; line-height:1; }
 .role{ left:31mm; top:14.2mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .rows{ left:31mm; top:22.5mm; }
 .row{ margin-bottom:2.2mm; }
 .k{ display:block; font-size:1.4mm; letter-spacing:.24em; color:var(--faint); margin-bottom:.4mm; }
 .v{ display:block; font-size:2.5mm; }
"""
rows = ''.join('<div class="row"><span class="k caps">%s</span><span class="v">%s</span></div>' % (k, v) for k, v in [('Telefon', TEL), ('E-Mail', MAIL), ('Web', WEB)])
body = ('<div class="bar"></div><div class="t"><p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p>'
        '<div class="qr" style="left:6mm;top:50%%;transform:translateY(-50%%);width:21mm;height:21mm">%s</div><div class="abs rows">%s</div></div>') % (QR, rows)
save(7, 'r', doc('07r', css, body))

# ---------- 08 Hell ----------
save(8, 'v', fix('visitenkarte-2026-vorne.html', light=True))
save(8, 'r', fix('visitenkarte-2026-hinten.html', light=True))

# ---------- 09 Leistungsleiste ----------
css = """
 .word{ position:absolute; left:7.5mm; top:13mm; font-family:var(--script); font-size:12.5mm; line-height:1; }
 .loc{ position:absolute; right:7.5mm; top:9mm; font-size:1.7mm; letter-spacing:.3em; color:var(--dim); }
 .tab{ position:absolute; left:7.5mm; right:7.5mm; bottom:8mm; display:grid; grid-template-columns:repeat(3,1fr); border-top:.25mm solid var(--line); }
 .tab span{ padding:2.4mm 0 0; text-align:center; font-size:1.65mm; letter-spacing:.24em; color:var(--ink); border-left:.25mm solid var(--line); }
 .tab span:first-child{ border-left:0; }
"""
save(9, 'v', doc('09v', css, '<div class="t"><div class="frame"></div><p class="word">Nadel &amp; Zwirn</p><p class="loc caps">Klagenfurt</p><div class="tab"><span class="caps">Firmenlogos</span><span class="caps">Caps &amp; Mützen</span><span class="caps">Textilien</span></div></div>'))
css = """
 .name{ left:8mm; top:8.5mm; font-family:var(--disp); text-transform:uppercase; font-size:4.6mm; line-height:1; }
 .role{ left:8mm; top:14.2mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .rows{ left:8mm; top:23mm; }
 .row{ display:flex; align-items:center; height:5.4mm; font-size:2.5mm; }
 .ic{ width:4.6mm; height:4.6mm; border:.3mm solid var(--red); border-radius:50%; color:var(--red); display:flex; align-items:center; justify-content:center; margin-right:2.6mm; }
 .ic svg{ width:2.3mm; height:2.3mm; }
"""
body = ('<div class="t"><div class="frame"></div><p class="abs name">Raphael Gritsch</p><p class="abs role caps">Gründer</p><div class="abs rows">%s</div>'
        '<div class="qr" style="right:8mm;top:50%%;transform:translateY(-38%%);width:17mm;height:17mm">%s</div></div>') % (rows_icons([(PH, TEL), (ML, MAIL), (GL, WEB), (PN, ORT)]), QR)
save(9, 'r', doc('09r', css, body))

# ---------- 10 Slogan plakativ ----------
css = """
 .slogan{ position:absolute; left:8mm; top:9mm; font-family:var(--disp); text-transform:uppercase; font-size:5.6mm; line-height:1.04; }
 .slogan i{ font-style:normal; color:var(--red); }
 .rl{ position:absolute; left:8mm; bottom:14.4mm; width:9mm; border-top:.5mm solid var(--red); }
 .wm{ position:absolute; left:8mm; bottom:7mm; font-family:var(--script); font-size:6.4mm; line-height:1; }
 .loc{ position:absolute; right:8mm; bottom:8mm; font-size:1.6mm; letter-spacing:.3em; color:var(--dim); }
"""
save(10, 'v', doc('10v', css, '<div class="t"><div class="frame"></div><p class="slogan">Stickerei,<br>die hält was<br>sie bestickt<i>.</i></p><div class="rl"></div><p class="wm">Nadel &amp; Zwirn</p><p class="loc caps">Klagenfurt</p></div>'))
css = """
 .name{ left:8mm; top:8mm; font-family:var(--disp); text-transform:uppercase; font-size:5.2mm; line-height:1.02; }
 .role{ left:8mm; top:19.4mm; font-size:1.8mm; letter-spacing:.24em; color:var(--red); }
 .hl{ position:absolute; left:8mm; right:8mm; top:28mm; border-top:.25mm solid var(--line); }
 .rows{ left:8mm; top:30.2mm; font-size:2.45mm; line-height:4.5mm; }
"""
body = ('<div class="t"><div class="frame"></div><p class="abs name">Raphael<br>Gritsch</p><p class="abs role caps">Gründer</p>'
        '<div class="qr" style="right:8mm;top:8mm;width:16mm;height:16mm">%s</div><div class="hl"></div>'
        '<div class="abs rows"><p>%s</p><p>%s</p><p>%s</p><p>%s</p></div></div>') % (QR, TEL, MAIL, WEB, ORT)
save(10, 'r', doc('10r', css, body))
print('ok')
