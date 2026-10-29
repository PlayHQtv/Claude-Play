# PlayHQ META carousel template (design v3 "digital HUD")

Approved 29.10.2026. Generates a full TikTok photo carousel (1080x1920 JPG): cover, one slide per weapon, CTA.
Only free components: Anton + Rajdhani (SIL OFL, licenses in assets/fonts), own textures (topo.png, grunge.png),
own gold HUD line icons (icons.py), ISNet background removal (rembg project, Apache-2.0) via onnxruntime.

## New carousel in 3 steps
1. Weapon images: `python3 cutout.py raw.png weapons/<name>.png` (game screenshot, any background).
2. Copy `data/2026-10-29-mw4-top4.json`, edit titles/ranks/attachments. Attachment `type` = an icon in assets/icons
   (barrel, muzzle, optic, underbarrel, reargrip, stock, magazine, ammo, apex, laser, comb). New type -> add to icons.py.
   `brightness` per weapon lifts dark renders (Kastov 1.7).
3. `python3 render.py data/<file>.json` -> out/<file>/01_cover.jpg ... NN_cta.jpg

Titles auto-fit (one line up to 10 chars, otherwise two lines white/gold). Needs python playwright + chromium.
