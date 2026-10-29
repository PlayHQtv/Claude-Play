# PlayHQ free toolbox

Rule: only permanently free tools. That means open source, or a free tier that allows commercial use. No trials, no subscriptions, no credit card.
"Status" says whether a tool is already set up in this repo.

| Tool | What it does for us | License | Where it runs | Status |
|---|---|---|---|---|
| ISNet (rembg models) | Cuts weapons and objects out of their background | Apache-2.0 | sandbox (onnxruntime), `templates/meta-carousel/cutout.py` | in use |
| Playwright + ffmpeg | Renders slides (HTML → JPG) and builds videos | Apache-2.0 / LGPL | sandbox | in use |
| Kokoro | AI voice (English, natural) | Apache-2.0 | GitHub Action `tts` | in use (parked route) |
| ACE-Step 1.5 | AI music like Suno (text → instrumental) | MIT | GitHub Action `music-ai` (CPU, ~7 min per 70 s track) | tested 29.10. |
| fetch-media | Downloads blocked URLs into the repo | – | GitHub Action `fetch-media` | in use |
| **PySceneDetect** | Finds scene changes and action moments in long gameplay videos, so the best clips can be picked faster without OpusClip credits | BSD-3 | – | noted only (user 29.10.: OpusClip already does this) |
| **Demucs** (Meta) | Separates voice / game sound / music. Removes copyrighted music from clips; makes voices clearer | MIT | GitHub Action (PyTorch) | to set up |
| **faster-whisper / WhisperX** | Word-accurate captions from real speech in PlayHQ style | MIT / BSD | GitHub Action | to set up |
| **Real-ESRGAN** | AI upscaling for blurry images and video stills (e.g. weapon renders) | BSD-3 | GitHub Action (ncnn-vulkan CPU build or PyTorch) | to set up |
| **auto-editor** | Gently cuts silence and idle time out of videos (alternative to OpusClip remove_pauses, which breaks gameplay clips) | Unlicense | GitHub Action / pip | to set up |
| Chatterbox (Resemble AI) | Clones our own voice from ~10 s of audio, with emotion control | MIT | GitHub Action (PyTorch) | later, own voice only |
| OpenVoice v2 | Voice cloning (simpler) | MIT | GitHub Action | later |
| Remotion | Animated video templates in React | free for individuals / teams of ≤3 | GitHub Action (Node) | later |
| Piper | Fast TTS, also German | MIT/GPL | GitHub Action | backup to Kokoro |
| Stable Audio Open Small | Text → music / SFX | Stability Community (free < $1M revenue), needs a free HF account | GitHub Action | alternative |
| Pixabay Music | Royalty-free tracks, commercial use OK | Pixabay Content License | the user downloads them (blocked for bots) | in use (parked route) |

## MCP connectors
- **Parallel Search** (free, no login): web search and page fetch. Use it for build research and the accuracy check when the normal WebFetch is blocked. Connected 29.10.

## Not allowed / avoid
- Non-commercial models: XTTS-v2, F5-TTS, MusicGen, the Suno free tier.
- Paid or trial-only tools: ElevenLabs, JsonCut beyond its free quota, Semrush, TinyFish, Orshot, Riverside, Tella.
- vidIQ (excluded by the user), anything that needs a Google account.
- Unofficial TikTok scrapers (account risk). Downloaders for other people's videos without permission.
