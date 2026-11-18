"""Render own 3D voxel scenes (mc_scene.html, three.js) to _build/mc/<name>.png.
Usage: python3 mc_scene.py scenes.json   (scenes.json = {"name": {params...}, ...})
Params: theme (meadow|desert|copper|fortress|cave|nether|frost), tier or heroes[], cam, look, fov, lights[], seed, exposure."""
import base64, json, os, sys, urllib.parse
import render as R


def main(spec_path, only=None):
    spec = json.load(open(spec_path))
    out = os.path.join(R.HERE, '_build', 'mc'); os.makedirs(out, exist_ok=True)
    srv = R.serve(R.HERE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1440})
        for name, prm in spec.items():
            if only and name not in only.split(','):
                continue
            prm = {'pr': 2, **prm}
            pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/mc_scene.html?n={name}#' + urllib.parse.quote(json.dumps(prm)),
                    wait_until='commit', timeout=240000)
            pg.wait_for_selector('body[data-ready]', timeout=240000)
            data = pg.evaluate('window.__png').split(',', 1)[1]
            fn = os.path.join(out, name + '.png'); open(fn, 'wb').write(base64.b64decode(data)); print(fn)
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main(*sys.argv[1:])
