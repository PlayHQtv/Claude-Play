"""PlayHQ FX video: animated 9:16 overlay (Playwright, transparent PNG frames) + graded/punched 16:9 clip (ffmpeg).
Usage: python3 render_fx.py <src.mp4> <out.mp4> [fx.json]
fx.json (optional): {"punches":[...], "kills":[...], "wanted":[start,end]} in seconds.
Video FX: colour grade + clarity + soft glow, zoom punch + shake on the punch times. Audio: loudnorm -14 LUFS + a low impact on the hook.
The source clip is never committed (third-party footage)."""
import json, os, sys, subprocess, shutil, functools, http.server, socketserver, threading

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'meta-carousel')
FPS = 30


def sh(*a):
    subprocess.run(a, check=True)


def probe_dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).strip())


def render_overlay(fx, work, n):
    html = open(os.path.join(HERE, 'fx_overlay.html')).read().replace('<script>', f'<script>window.FX={json.dumps(fx)};</script><script>', 1)
    os.makedirs(os.path.join(ASSETS, '_build'), exist_ok=True)
    open(os.path.join(ASSETS, '_build', 'fx_overlay.html'), 'w').write(html)
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ASSETS); h.log_message = lambda *a: None
    srv = socketserver.TCPServer(('127.0.0.1', 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/_build/fx_overlay.html'); pg.wait_for_selector('body[data-ready]')
        for f in range(n):
            pg.evaluate(f'draw({f / FPS})')
            pg.screenshot(path=f'{work}/ov/{f:05d}.png', omit_background=True)
        b.close()
    srv.shutdown()


def main(src, out, fxp=None):
    fx = json.load(open(fxp)) if fxp else {}
    dur = round(probe_dur(src) - 0.05, 2)
    fx.setdefault('punches', [0, 2.85, 5.27, 6.71, 9.96, 17.47, 19.10, 20.69])
    fx.setdefault('kills', [3.9, 4.25, 4.6, 4.95])
    fx.setdefault('wanted', [6.6, 10.2])
    fx['dur'] = dur
    work = os.path.join(HERE, '_work'); reuse = os.environ.get('REUSE_OVERLAY') and os.path.isdir(work + '/ov')
    if not reuse:
        shutil.rmtree(work, ignore_errors=True); os.makedirs(work + '/ov')
    # 1) overlay frames
    n = int(dur * FPS)
    if not reuse:
      render_overlay(fx, work, n)
    # 2) zoom punch + shake expression (strength decays over 0.35 s after each punch)
    terms = '+'.join(f"if(between(t,{p},{p}+0.35),(1-(t-{p})/0.35),0)" for p in fx['punches'])
    k = f"min(1,{terms})"
    z = f"(1+0.14*{k})"
    sx = f"(12*{k}*sin(t*95))"; sy = f"(9*{k}*cos(t*83))"
    vf = (f"fps={FPS},scale=1920:1080:flags=lanczos,"
          f"crop=w='iw/{z}':h='ih/{z}':x='(iw-iw/{z})/2+{sx}':y='(ih-ih/{z})/2+{sy}',"
          "scale=1080:608:flags=lanczos,"
          "eq=contrast=1.10:saturation=1.16:gamma=0.98,"
          "colorbalance=rm=0.02:bm=-0.02:rh=0.03:bh=-0.03,"
          "unsharp=5:5:0.9:3:3:0.3,"
          "split[a][g];[g]gblur=sigma=14,eq=brightness=-0.10[gb];[a][gb]blend=all_mode=screen:all_opacity=0.12,"
          "vignette=angle=PI/5,"
          "pad=1080:1920:0:656:color=0x070707[v];"
          f"[v][1:v]overlay=0:0:format=auto,format=yuv420p[vo]")
    af = ("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[voice];"
          "aevalsrc='0.9*sin(2*PI*(38+60*exp(-t*9))*t)*exp(-t*5)':d=0.9:s=48000,aformat=channel_layouts=stereo,volume=0.35[imp];"
          "anoisesrc=d=0.45:c=pink:r=48000:a=0.5,highpass=f=900,lowpass=f=6000,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.15,aformat=channel_layouts=stereo,volume=0.18[wh];"
          "[voice][imp][wh]amix=inputs=3:normalize=0:duration=first[ao]")
    sh('ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-framerate', str(FPS), '-i', f'{work}/ov/%05d.png',
       '-filter_complex', vf + ';' + af, '-map', '[vo]', '-map', '[ao]', '-t', str(dur),
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out)
    print(out)


if __name__ == '__main__':
    main(*sys.argv[1:])
