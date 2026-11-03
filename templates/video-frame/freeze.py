"""PlayHQ FREEZE + MARKUP for framed 16:9 videos (user rule 03.11.2026: every framed video gets this).

Flow in the finished video:
  1. clip plays normally (hook in the frame's top band)
  2. at the key moment the picture freezes ~3 s, "PAUSED" tag top right, sound bed plays (sfx.py: whoosh, tick, pop per markup, hit on the banner)
  3. markups pop in one after another (circle/box with label + arrow), last step = verdict banner
  4. clip continues
The whole video also gets the animated PlayHQ logo (logo_anim.py, rotating ring + beat + sheen) over the frame's static logo.

Usage: python3 freeze.py freeze_jobs/<name>.json <in.mp4> <out.mp4>
Job JSON (coordinates in VIDEO-WINDOW pixels, window = 1080x608 at y=video_top of the 1080x1920 frame):
{"t": 13.5, "video_top": 656,
 "steps": [
   {"kind": "circle", "x": 530, "y": 280, "r": 95, "label": "FINAL EXFIL CHOPPER", "lx": 640, "ly": 120},
   {"kind": "box", "box": [40,160,140,196], "label": "RADIATION CLOSING IN", "lx": 40, "ly": 96, "color": "red"}
 ],
 "banner": "ALL OTHER EXFILS = GONE",
 "durations": [0.5, 0.8, 0.8, 1.1]}
The input/output videos are third-party footage -> keep them OUTSIDE the repo (scratchpad).
"""
import json, os, subprocess, sys, tempfile, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfx, logo_anim
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'meta-carousel', 'assets', 'fonts', 'Anton-Regular.ttf')
Y, K, W_, R = (255, 212, 0), (0, 0, 0), (255, 255, 255), (255, 75, 62)
F40, F34 = ImageFont.truetype(FONT, 40), ImageFont.truetype(FONT, 34)


def tag(d, x, y, text, font, bg, fg):
    w = d.textlength(text, font=font); h = font.size + 14
    x = max(4, min(x, 1076 - w - 24))
    d.rectangle((x, y, x + w + 24, y + h), fill=bg)
    d.text((x + 12, y + h / 2), text, font=font, fill=fg, anchor='lm')
    return x, y, x + w + 24, y + h


def arrow(d, x1, y1, x2, y2, col):
    d.line((x1, y1, x2, y2), fill=col, width=7)
    a = math.atan2(y2 - y1, x2 - x1)
    p = [(x2, y2), (x2 - 26 * math.cos(a - .45), y2 - 26 * math.sin(a - .45)), (x2 - 26 * math.cos(a + .45), y2 - 26 * math.sin(a + .45))]
    d.polygon(p, fill=col)


def draw_step(d, s):
    col = R if s.get('color') == 'red' else Y
    fg = W_ if col == R else K
    if s['kind'] == 'circle':
        x, y, r = s['x'], s['y'], s['r']
        d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=8)
        tx = (x - r, y - r, x + r, y + r)
    else:
        tx = tuple(s['box'])
        d.rectangle(tx, outline=col, width=6)
    if s.get('label'):
        b = tag(d, s['lx'], s['ly'], s['label'], F40 if len(s['label']) < 22 else F34, col, fg)
        # arrow from label to the nearest point of the target
        cx, cy = (b[0] + b[2]) / 2, b[3] if b[3] < tx[1] else b[1]
        if b[3] < tx[1] or b[1] > tx[3]:
            ty = tx[1] - 6 if b[3] < tx[1] else tx[3] + 6
            txx = min(max(cx, tx[0] + 20), tx[2] - 20)
            if abs(ty - cy) > 30:
                arrow(d, cx, cy + (4 if b[3] < tx[1] else -4), txx, ty, col)


def frames(job, still):
    vt = job.get('video_top', 656)
    base = still.convert('RGB')
    win = ImageEnhance.Brightness(base.crop((0, vt, 1080, vt + 608))).enhance(0.82)
    out, layers = [], [None] + job['steps'] + ['banner']
    for i in range(len(layers)):
        w = win.copy(); d = ImageDraw.Draw(w, 'RGBA')
        d.rectangle((920, 14, 1066, 62), fill=(0, 0, 0, 215)); d.text((993, 38), 'PAUSED', font=F34, fill=Y, anchor='mm')
        for s in layers[1:i + 1]:
            if s == 'banner':
                # covers the burned-in caption line of the clip (min 680 px wide, 84 px high)
                t = job['banner']; tw = max(d.textlength(t, font=F40), 640)
                by, bx = job.get('banner_y', 494), job.get('banner_x', 540)
                d.rectangle((bx - tw / 2 - 20, by, bx + tw / 2 + 20, by + 84), fill=(0, 0, 0, 255))
                d.rectangle((bx - tw / 2 - 20, by, bx - tw / 2 - 10, by + 84), fill=Y)
                d.text((bx, by + 42), t, font=F40, fill=W_, anchor='mm')
            else:
                draw_step(d, s)
        im = base.copy(); im.paste(w, (0, vt)); out.append(im)
    return out


def run(cmd):
    subprocess.run(cmd, check=True)


def main(job_path, src, dst):
    job = json.load(open(job_path)); t = float(job['t'])
    dur = job.get('durations') or [0.5] + [0.8] * len(job['steps']) + [1.1]
    with tempfile.TemporaryDirectory() as tmp:
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', src, '-frames:v', '1', f'{tmp}/still.png'])
        imgs = frames(job, Image.open(f'{tmp}/still.png'))
        lst = open(f'{tmp}/l.txt', 'w')
        for i, (im, du) in enumerate(zip(imgs, dur)):
            im.save(f'{tmp}/s{i}.png'); lst.write(f"file 's{i}.png'\nduration {du}\n")
        lst.write(f"file 's{len(imgs) - 1}.png'\n"); lst.close()
        fr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip() or '30/1'
        hold = sum(dur)
        # sound bed instead of silence, level matched to the clip (peak of the clip's audio * 0.6)
        pk = subprocess.run(['ffmpeg', '-v', 'info', '-i', src, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
        mx = next((float(l.split(':')[1].split()[0]) for l in pk.splitlines() if 'max_volume' in l), -3.0)
        sfx.make(dur, f'{tmp}/bed.wav', level=min(0.9, 10 ** (mx / 20) * job.get('sfx_gain', 0.6)))
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt',
             '-i', f'{tmp}/bed.wav',
             '-vf', f'fps={fr},format=yuv420p,trim=duration={hold}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
             '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{tmp}/hold.mp4'])
        fc = (f'[0:v]trim=0:{t},setpts=PTS-STARTPTS,fps={fr},format=yuv420p[v0];[0:a]atrim=0:{t},asetpts=PTS-STARTPTS,aresample=48000[a0];'
              f'[1:v]setpts=PTS-STARTPTS,fps={fr},format=yuv420p[v1];[1:a]asetpts=PTS-STARTPTS,aresample=48000[a1];'
              f'[0:v]trim=start={t},setpts=PTS-STARTPTS,fps={fr},format=yuv420p[v2];[0:a]atrim=start={t},asetpts=PTS-STARTPTS,aresample=48000[a2];'
              '[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[vc][a];'
              f'[2:v]fps={fr},format=yuv420p[lg];[vc][lg]overlay=880:140:shortest=1[v]')  # animated logo over the static one
        run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-i', f'{tmp}/hold.mp4', '-stream_loop', '-1', '-i', logo_anim.get(), '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dst])
        imgs[-1].save(os.path.splitext(dst)[0] + '_freeze.jpg', quality=92)
    print(dst)


if __name__ == '__main__':
    main(*sys.argv[1:])
