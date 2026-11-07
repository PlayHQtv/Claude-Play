# Remotion + GSAP "Anatomy" weapon breakdown (PlayHQ)
- Job: `remotion/jobs/<date>-<name>.json` (weapon image path, title, parts with image coords px/py + tag position, sfx list from `assets/sfx/kenney/` (CC0), bed audio).
- Push the job to `brand-assets` → workflow `remotion-render` (npm installs remotion@4 + gsap@3 on the runner, `prep.py` builds public/, renders 1080×1920 30 fps) → MP4 in the draft release `renders`, log in `remotion/logs/`.
- Part coords: measure on the weapon PNG (pixel coords of the original image). Rifle is laid out 1000 px wide at x 40, centred on y 900.
- All motion = one paused GSAP timeline seeked per frame (SplitText, DrawSVG). Sounds: Kenney Sci-Fi (CC0) + own synthesized bed.
