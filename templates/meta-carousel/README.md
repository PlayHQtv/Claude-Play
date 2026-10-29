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

## Accuracy rule (mandatory, 29.10.2026)
Never take attachment names from old slides or memory. Before every preview:
1. Pull builds from codmunity.gg (DMZ: /best-loadouts/mw4-dmz/long-range and /close-range; MP: /weapon/mw4/<weapon>),
   note "Last Updated" date; cross-check names with a second site (warzoneloadout.games, wzstats.gg) where possible.
2. Copy names, slot labels and build codes exactly; record the source in the data JSON ("source").
3. No "top/rank" claims the data doesn't support (use rank_label "BUILD" when it's just list order).
4. Run an independent verifier agent that re-fetches the sources and checks every slide character by character.

## Hashtags for build carousels (user 29.10.2026)
Use `#mw4 #mw4dmz #dmz #dmztips #dmzloadout` (same pattern as the "5 MW4 DMZ mistakes" carousel: game, game+mode, mode, mode-tips, topic).
NOT `#mw4builds #codmeta #mw4meta`: too narrow, and they leave the DMZ audience out. The 29.10. carousel was deleted and reposted because of this.
Caption must start with the search phrase, e.g. "MW4 DMZ meta builds: …".
