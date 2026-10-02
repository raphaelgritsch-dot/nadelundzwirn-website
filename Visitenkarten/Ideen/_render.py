import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

here = os.path.dirname(os.path.abspath(__file__))
E = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
tmp = os.path.join(os.environ['TEMP'], 'vk-ideen')
os.makedirs(tmp, exist_ok=True)

ids = [int(a) for a in sys.argv[1:]] or list(range(1, 11))
for n in ids:
    for side in ('v', 'r'):
        src = os.path.join(here, 'idee-%02d-%s.html' % (n, side))
        out = os.path.join(here, 'idee-%02d-%s.png' % (n, side))
        url = 'file:///' + src.replace('\\', '/').replace(' ', '%20').replace('ä', '%C3%A4')
        subprocess.run([E, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2.5',
                        '--window-size=337,223', '--virtual-time-budget=3000', '--screenshot=' + out, url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sheet(nums, name):
    ims = []
    for n in nums:
        a = Image.open(os.path.join(here, 'idee-%02d-v.png' % n)).convert('RGB')
        b = Image.open(os.path.join(here, 'idee-%02d-r.png' % n)).convert('RGB')
        ims.append((n, a, b))
    w, h = ims[0][1].size
    pad = 40
    top = 70
    W = pad * 3 + w * 2 + 90
    H = top + len(ims) * (h + pad)
    out = Image.new('RGB', (W, H), (92, 92, 92))
    d = ImageDraw.Draw(out)
    try:
        f = ImageFont.truetype('arialbd.ttf', 44)
    except Exception:
        f = ImageFont.load_default()
    for i, (n, a, b) in enumerate(ims):
        y = top + i * (h + pad)
        d.text((20, y + h // 2 - 22), '%02d' % n, fill=(255, 255, 255), font=f)
        out.paste(a, (90, y))
        out.paste(b, (90 + w + pad, y))
    out.save(os.path.join(here, name))
    print(name, out.size)


if len(ids) == 10:
    sheet(range(1, 6), 'ideen-1-bis-5.png')
    sheet(range(6, 11), 'ideen-6-bis-10.png')
