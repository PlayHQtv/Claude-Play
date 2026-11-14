# External tools (added 14.11.2026, user: "Hole dir diese Tools aus Prinzip einmal")

Install everything with `bin/ext_tools.sh` (pinned versions, nothing third-party is committed).

| Tool | Source / licence | Status here | What we use it for |
|---|---|---|---|
| **RealSFX** (real-sfx skill) | Clipwing/skills, MIT; uisfx sounds CC0 | works (CPU), connected to our library `assets/sfx` (229 CC0 sounds) | sound design for future videos: real recorded SFX on the exact frame, separate WAV + report |
| **Openverse API** | api.openverse.org, no key | works through workflow `openverse-sfx` (sandbox has no direct access) | new CC0 sounds: add `name \| query \| max seconds` to `assets/sfx/openverse.txt`, credits in `assets/sfx/openverse/CREDITS.txt` |
| **sfx_place.py** (own) | this repo | works | quick exact-frame placement: `bin/sfx_place.py in.mp4 out.mp4 F12:whoosh 2.5s:pop:-6` |
| **PhotoCraft** (photocraft-cli + MCP) | storytold/photocraft v0.23.1, Apache-2.0 | works headless (CPU): 1009 engine commands, PSD export, Smart Sharpen, Remove Background | optional: PSD exports of slides, batch adjustments; MCP: `photocraft-cli mcp --headless --automation-read-root <dir> --automation-write-root <dir>` |
| **Find Skills** | vercel-labs/skills, MIT | skill text available; `npx skills find` gets no results here (skills.sh blocked) | finding new skills: use GitHub search instead |
| **VoiceStudio** | debpalash/VoiceStudio, AGPL-3.0 | not installed by default (needs GPU + model downloads; HuggingFace blocked) | only for future voice-over videos, on request |

Rule (user 09.11.): tools are only used when they clearly improve the content. Carousels stay silent images
(autoAddMusic), so the SFX tools are for videos only.
