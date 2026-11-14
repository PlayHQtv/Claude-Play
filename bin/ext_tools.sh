#!/bin/bash
# Installs the external tools (pinned, never committed) into ${PHQ_EXT:-/tmp/ext}:
#   real-sfx     Clipwing/skills (MIT)  - real sound effects on the exact frame, connected to assets/sfx (CC0 library)
#   find-skills  vercel-labs/skills (MIT) - how to search the skills ecosystem (npx skills find; skills.sh may be blocked here)
#   photocraft   storytold/photocraft v0.23.1 (Apache-2.0) - headless photo editor CLI + MCP (1000+ commands)
#   voicestudio  debpalash/VoiceStudio (AGPL-3.0) - local TTS/voice cloning; code only, needs GPU + models -> only on request
# Usage: bin/ext_tools.sh [voicestudio]
set -e
E=${PHQ_EXT:-/tmp/ext}; ROOT=$(cd "$(dirname "$0")/.." && pwd); mkdir -p "$E/bin"
pin(){ [ -d "$E/$2/.git" ] || { git clone -q --filter=blob:none https://github.com/$1 "$E/$2" && git -C "$E/$2" checkout -q $3; }; }
pin Clipwing/skills clipwing edbefcbc3474
pin vercel-labs/skills vercel b716f9dc2ba3
S=$E/clipwing/skills/real-sfx
(cd "$S" && python3 scripts/setup.py check >/dev/null 2>&1; grep -q '"playhq"' config.json 2>/dev/null || python3 scripts/setup.py add-library playhq "$ROOT/assets/sfx" --tier main --index >/dev/null)
if [ ! -x "$E/bin/photocraft-cli" ]; then
  R=repos/PlayHQtv/Claude-Play; rid=$(gh api "$R/releases" -q '.[]|select(.name=="grab-private")|.id' | head -1)
  for pg in 1 2 3 4; do id=$(gh api "$R/releases/$rid/assets?per_page=100&page=$pg" -q '.[]|select(.name=="photocraft-cli")|.id'); [ -n "$id" ] && break; done
  gh api -H "Accept: application/octet-stream" "$R/releases/assets/$id" > "$E/bin/photocraft-cli" && chmod +x "$E/bin/photocraft-cli"
fi
[ "$1" = voicestudio ] && pin debpalash/VoiceStudio voicestudio 7a261cc2165b
echo "real-sfx:   $S   (python3 scripts/setup.py check)"
echo "photocraft: $("$E/bin/photocraft-cli" --version)"
echo "sfx place:  bin/sfx_place.py   |  Openverse CC0: add lines to assets/sfx/openverse.txt"
