---
name: "playhq-tiktok-clips"
description: "Setup, rules and workflow for the <OUR_TIKTOK_HANDLE> TikTok gaming account: Metricool analytics, OpusClip clip editing, Cloudinary covers, verified META build carousels (GitHub template), and auto-posting via Metricool."
---

# <OUR_TIKTOK_HANDLE> TikTok clip workflow

Always answer the user in German. The user wants to do as little as possible himself: prepare, edit and schedule posts autonomously, then report briefly (daily). Goal: **maximum reach / clicks** ("Wir müssen vom Algorithmus gepusht werden", "Bedenke alles Gelernte"). Continuous improvement based on ALL data.

## PRE-PUBLISH GATE (user 29.10.: "So etwas darf nicht mehr passieren") – nothing goes to Metricool before ALL of these pass
1. **Facts** verified against the live source (no memory/old slides) + independent verifier agent PASS.
2. **Display check in the real TikTok view:** photo posts are shown as **3:4** (TikTok crops 9:16 photos top and bottom – 29.10. carousel lost its header and the 3rd tile row). Carousels are rendered at **1080×1440** and checked with `tiktok_overlay.py` (search bar/tabs top, "2/6" counter top-right, avatar/like/comment/save column right from y≈1100, first-comment bubble bottom-left). Videos: hook/captions not under the right button column or the caption area.
3. **Hashtags** match HASHTAGS v3 (game + game-mode + mode + mode-tips + topic). Never ship a post whose tags miss the mode (#dmz/#mw4dmz) – 29.10. META carousel had `#mw4builds #codmeta #mw4meta` → "viel zu eng", user deleted it.
4. **Caption** starts with the search phrase; title + first comment set; `autoAddMusic: true` for every photo/carousel post.
5. **Cover/frames** contain no burned-in captions or profanity (crop the still if needed) and are checked visually (fetch the Cloudinary result via the GitHub fetch-media workflow and Read it).
6. **No duplicates:** check getScheduledPosts for the same media/topic in other slots (29.10.: "Pay to win?" was scheduled both Fri 10:00 and 18:00). A repost after deleting/privating a post must be visibly changed (new cover wording, title, caption, first comment) so TikTok doesn't see a duplicate.
7. **Display quality (user 30.10.: "Insgesamt brauchen wir immer hohe Anzeige-Qualität"; "1080p Upscaling reicht vorerst für jeden Content der darunter liegt"):** every video, slide and cover must be at least 1080p (videos 1080×1920, carousels 1080×1440, covers 1080×1920).
   - Always use the OpusClip **HD export**, never the 720p preview, for media and cover stills.
   - Check the width/height of every source (Cloudinary upload response).
   - Anything below 1080p gets upscaled to 1080p:
     - stills and renders: Lanczos + light unsharp, or Real-ESRGAN via GitHub Action;
     - video: Cloudinary `c_scale` to 1080 wide + `e_sharpen:40`, or ffmpeg `lanczos` + `unsharp`.
   - Encode at q_90 / crf ≤18.
8. **Timing (user 30.10.: "Poste nur anhand der Statistik", "Es müssen immer zwischen 5–6 Stunden dazwischen liegen"):** see POSTING TIMES.

## POSTING TIMES (user 30.10., based on data – re-check weekly)
- **Standard: 12:00 + 18:00 every day** (6 h gap).
  - Metricool best-time (Berlin): peaks at 10, 12 and 18 h on all days; weekdays ~1,050–1,470, weekend ~700–850; after 20 h it drops (21 h ~470–640).
  - Our own 47 posts (median views): 18 h 932 (19 posts, most reliable), 12 h 877 (both 5K breakouts), 10 h only 618, 19 h+ 606.
- Weekends: put the strongest piece at 12:00 (weekend activity 12 h > 18 h).
- **Min. gap between posts: 5–6 h → max 2 posts/day.** Extra content (e.g. an extra carousel) goes to the next free slot on another day, never into a weak hour.
- Re-run getBestTimeToPostByNetwork + our per-slot medians weekly. Report it if 10:00 with strong topics beats 12:00.

## Accounts & IDs
- TikTok: <OUR_TIKTOK_HANDLE> – **PERSONAL account** (confirmed by user screenshot 28.10.; the old "Business account" note was wrong). Started ~03.10.2026. Custom covers via Metricool videoThumbnailUrl DO show on the profile (checked 28.10.). Creator Rewards Program needs 10K followers, 100K views/30 days, 18+, personal account, original videos >1 min.
- Metricool: brandId/blogId `<METRICOOL_BLOG_ID>`, timezone `Europe/Berlin`. **Starter plan since 19.10.2026 (unlimited posts).** User has the Metricool app since ~23.10. but wants no push publishing ("mach gar nix") → always `autoPublish:true`. YouTube not connected in Metricool. User 30.10.: no YouTube Shorts / Instagram cross-posting ("Nein") – TikTok only.
- OpusClip: TikTok post account `<ACCOUNT_ID>`, YouTube `<ACCOUNT_ID>` (PlayHQ; posting only, no search). PRO plan – save credits (no needless submits; user uploads sources himself).
- Cloudinary: cloud `<CLOUDINARY_CLOUD>`, free plan (max upload 100 MB). Only for covers; delete files after use.
- Old scheduled task "TikTok-Autopilot" `<TRIGGER_ID>` (08:58 Berlin) still runs with OLD rules (may add CS posts); update_trigger is rejected. Workaround: daily send_later morning check 09:30 Berlin (07:30Z summer / 08:30Z winter from 25.10.) that replaces its posts (updateScheduledPost) and creates the next send_later. Don't delete triggers without asking (user rejected that once).
- Never connect Google; vidIQ excluded. Whop only free content. Never send the user's email anywhere.
- **FREE TOOLS ONLY (user 29.10.: "Die Sachen sollten immer kostenlos bleiben ohne seltsame Testabos"):** only permanently free tools (open source / free tiers that allow commercial use). No trials, subscriptions or credit-card sign-ups; if a provider pushes a trial or payment data, skip it and tell the user. Watch licenses: non-commercial models (XTTS-v2, F5-TTS, MusicGen, Suno free tier) are NOT allowed for this monetization-aiming account. Full list: FREE TOOLBOX section + `TOOLS.md` in the repo. No CapCut connector exists (checked 30.10.); unofficial CapCut-desktop controllers need the user's PC and Pro features are paid → rebuild CapCut looks with ffmpeg/Cloudinary instead.

## Mix since 26.10. (user): views dropped with Waffles-only → back to CS:GO Cursed Weapons (@lichcs2, project <OPUSCLIP_PROJECT_ID> "1 HOUR OF CURSED WEAPONS IN CS"; used: Door Stuck <CLIP_ID>, Silenced Knife <CLIP_ID> + older copies). Max 1 MW4 post per day, other slot "sinnvoll" (CS cursed etc.). Skip sexual-content clips (Yondu arrow, Pumpoff, She-Grenade, HErection) and cut slurs/sexual remarks. Reserve MW4: keys-yet <CLIP_ID>.

- Asmongold (user wish 27.10.): project <OPUSCLIP_PROJECT_ID> "The Most Controversial Game of 2026" (Hood Warfare). <CLIP_ID> (bot excuse) was REJECTED by user ("der ist scheisse") and replaced on 28.10. 18:00 by MW4 bounty <CLIP_ID> (@MrMarvelTV, cover layout D "WANTED"). Be careful with Asmongold/Hood Warfare clips – user dislikes them. Remaining: <CLIP_ID>/<CLIP_ID> bag secured (long), <CLIP_ID>, <CLIP_ID>, <CLIP_ID> Lay's chips. Heavy profanity in game voice lines → cut sexual words. remove_pauses destroys gameplay clips with little speech (80 s → 8 s) – don't use it on gameplay-heavy clips. CS M4M clip <CLIP_ID> (exported, 33 s, cover idea layout B orange) now reserve.

## Scope change 26.10.2026 (user): "Unser ganzer Account wird sich mit Spielen aller Art befassen"
- Account = games of ALL kinds (not only MW4). MW4 DMZ stays the current running series until new sources come; new games need sources the user uploads (or well-known creators found by me, with clear credit).
- Hashtag scheme generalizes: 1 broad (#gaming or the game's franchise) + 1 adjacent community + 2 niche (game + mode) + 1 topic.
- Creator Search Insights findings 26.10. (content gaps / trends): "mw4 dmz gameplay" 297K (GAP) → use phrase + #dmzgameplay; "best 1v4 clutch" 179K +1000% (gap), "clutch gameplay" 114K (gap); "game mechanics that boost your progress" 10.7M +450%; "mw4 settings"/"setting mw4" +1000%, "fov mw4"; other-game gaps: warhammer 40k dawn of war 4 (168K), battlefield 1 dlss 5 (218K, +1000%), helperbot gameplay, showdown gameplay (376K), Minecraft fights, rust videos, active games, late night gaming. Map name is "Hajin" (not Hyazan).

## Content strategy history (CURRENT rules = FOCUS DECISION + ACCOUNT FORMAT above)
- 23.10.: only MW4 DMZ, Waffles both slots → views plateaued → 26.10. mix with CS/Asmongold → 28.10. focus ~80 % MW4 DMZ (rotating Waffles / SiNister / MrMarvel) + ~20 % other games.
- Never crop 16:9/1:1 videos or cover frames (original format).
- New sources: user uploads to OpusClip and sends a YouTube screenshot for the creator (new sources only from November). Own search: prefer **virality**, **well-known channels**, **high quality** (≥1080p, real gameplay). Creator must be clear for credit, otherwise don't post.

## What the data taught us (up to 22.10.)
- Best: "Stop fighting everything in MW4 DMZ" (stealth vs. fighting) **4,721 views, 98 likes, 18 comments, 14 shares, 16 saves**, two push waves; "#1 MW4 DMZ mistake" 1,498; "STOP! This body…" 880. Plain how-to without debate ("Do this before you loot") only ~370.
- Winning patterns: **polarizing topics** people want to argue about, **"mistake"/"STOP"** hooks that make viewers feel caught, useful tips that get saved.
- Weakness: viewers drop fast – 4K video avg watch 13.9 s of 29.5 s, only 21.8 % full views.
- 2 posts/day do not cannibalize; 4/day did. Midday slot slightly better than 18:00.
- Follow up a viral post quickly with a "Part 2" on the same topic, and ask the user to reply to comments in the first hours.
- Record day 20.10.: 5,601 views; followers 138 (22.10.).

## Hard rules for every post (checklist before scheduling)
1. **Credit** the original creator ALWAYS (`Credit: @handle`). Unclear → don't post.
2. **Retention-first edit** (user rule 23.10.):
   - **Cold open:** the strongest spoken line/payoff goes first (reorder_sections / delete intro phrases like "Now another thing…", "So…").
   - **Short hook in 2 stages:** 0–1.5 s max 4–6 words ("STOP DOING THIS"), 1.5–3.5 s the specific point ("in MW4 DMZ"). Readable in under a second. (16:9 clips: hook goes into the PLAYHQ VIDEO FRAME instead – see below.)
   - **Open loop** mid overlay ("the last part is the trick") only if the clip delivers it.
   - `remove_filler_words` + `remove_pauses` (**0.7 s**, keep the natural speech flow; only cut intro/outro and real filler, no choppy over-cutting).
   - Captions ON, NOT uppercase, keyword highlight (e.g. yellow `#ffd400`) via set_style + set_keyword_highlight.
   - Length **20–30 s** (user rule 24.10.: our data showed 29–30 s clips got ~13–14 s avg watch and the most views, while 18–19 s edits only got 7–9 s avg watch with no better completion; heavy cuts also risk "unoriginal/choppy" signals).
3. **Extreme hooks** (warning / loss / mistake / curiosity), never invented facts or stats; the video must deliver what the hook promises.
4. **SEO**: ONE main search phrase per video (e.g. "MW4 DMZ tips") in hook overlay, TikTok title, first sentence of description, captions; write "MW4" and "Modern Warfare 4 DMZ" and "Call of Duty". Natural sentences, no keyword spam.
5. **Hashtags exactly 5** – see HASHTAGS v3 below. No #fyp/#viral, no unrelated tags.
6. Small verdict "PLAYHQ X/10" overlay near the end (see #11). No emojis in the video (`set_emoji false`). Remove OpusClip auto-hook overlays if present (check overlay list).
7. Description: hook + SEO + "Save this…" + CTA (send to your squad) + credit + hashtags. **First comment = polarizing either/or question** ("Team stealth or team full send?").
8. New-style cover (below). Max 2 posts/day: **12:00 + 18:00 every day** (see POSTING TIMES; replaced 10:00 + 18:00 on 30.10.).
9. **Weekday/weekend split (user rule 24.10.):** audience activity on Sat/Sun is ~40 % lower than Wed/Thu, and all our hits landed Mon/Tue. Put the STRONGEST clips (polarizing, "STOP/mistake/don't buy" hooks) on Mon–Wed; weekends get calmer save-worthy/search tips (traits, keys, how-to). Keep 2 posts on weekends.
10. Comment question also as end overlay ("Money or XP? Comment") and "Comment below 👇" in the description. Overlays max 3–5 words, never two at once, all at the top. Captions NOT uppercase.
11. **Verdict small + short (user rule 26.10.):** overlay box width = text length (no font-size control), so verdict is just "PLAYHQ 9/10" for 1.5 s; end question 2–3 words ("Buy or upgrade?") for ~2 s at the very end. Engagement farming runs mainly via description + first comment.
12. **Scheduling autonomy (user 27.10.: "Plane selbstständig ein"):** prepare AND schedule posts on my own (no waiting for OK), then report clip, hook, cover, text and reasoning in the daily report. (Earlier rule 26.10. "show plan before uploading" is superseded; ask only for unusual decisions, e.g. new creator/game, or anything risky.)
13. **Search gaps:** use TikTok Creator Search Insights (Gaming, content-gap filter; search "DMZ", "MW4", "Modern Warfare 4") – via user screenshots or Claude in Chrome if available. Put gap terms into hook overlay, title, first sentence and as the 5th hashtag, only if the clip truly covers the topic.
14. **Caption SEO always (user rule 26.10.):** description = TikTok search text. Structure: (1) main search phrase exactly as people search it at the very start ("MW4 DMZ gameplay: …", "best … in MW4 DMZ"); (2) 1–2 natural sentences with 2–4 related keywords from Search Insights/web (Modern Warfare 4 DMZ, Call of Duty, Hajin, beginner guide/tips, the specific item/mechanic); (3) comment question; (4) save/share CTA; (5) credit; (6) 5 hashtags. Same phrase in title, hook overlay #2 and spoken/captions where possible. No keyword spam, no unrelated trending terms.
15. Hashtag scheme v2 (26.10., superseded by HASHTAGS v3): caption keywords (game name + what happens) matter more than many hashtags. A/B test #gaming (Mon 26.10.) vs #gamingontiktok (Tue 27.10.) was inconclusive.

## Always (user 28.10.): SEO on every post + video must stay mostly unobstructed (overlays short, small, top only, one at a time; captions not covering the action). First comment via Metricool firstCommentText IS published on TikTok (user confirmed 28.10.). First comment: no extra hashtags (on TikTok, hashtags in comments don't put the video on hashtag pages and look spammy); instead a natural question containing 1–2 search keywords (e.g. "Best MW4 DMZ key you found?").

## PLAYHQ VIDEO FRAME for 16:9 clips (user 29.10.: "unsere Einblendungen müssen weniger Platz einnehmen und nicht zu lange das Bild verdecken" + "nutze den leeren Platz oben und unten für unsere Overlays oder ein einheitliches Hintergrund-Design") – STANDARD for every landscape clip
- No OpusClip text overlays over the gameplay: remove them all (edit_clip remove_text_overlay, check with dryRun). Keep only the captions, with highlight in PlayHQ yellow (set_style highlightColor #FFD400 + set_keyword_highlight true, never the green default).
- The hook goes in the top band and the question in the bottom band, as a static branded frame. Template `templates/video-frame/frame.py` + `jobs/<date>-<name>.json`:
  - Fields: hook_white, hook_gold, kicker, badge, question, sub, video_top 656.
  - Output: 1080×1920 PNG with a transparent window (y 656–1264) and the same look as carousel v3 (black, gold topo, gold edges + yellow corner ticks, CALL OF DUTY · MW4 + DMZ badge, round logo).
  - Push to `brand-assets` → Cloudinary upload from the raw URL with the full SHA as `playhq/frames/<name>`.
- Composite in Cloudinary:
  - Export OpusClip HD (1920×1080) → upload as `playhq/work/<slot>_hd`.
  - Transform (video): `c_scale,w_1080/c_pad,w_1080,h_1920,b_rgb:<ID>/l_playhq:frames:<name>/fl_layer_apply,g_north/q_90/f_mp4` (~10 MB for 22 s).
  - Cover: the same chain plus `so_1` and a `.jpg` extension.
  - Use the derived secure_urls as Metricool media / videoThumbnailUrl.
- QA before the preview:
  - Fetch 3 frames via fetch-media and draw the 9:16 TikTok UI zones: top 0–170; right buttons x≥940, y 980–1660; caption x≤900, y≥1560.
  - Frame text only in y 190–600 and 1320–1500.
  - Send the QA sheet as the preview, then delete the frames from the public repo.
  - Metricool copy must match the derived file (bytes, 1080×1920).
- First use: 29.10. bounty <CLIP_ID> ("4 KILLS = / YOU'RE HUNTED", "HUNTER OR HUNTED?"), moved to 19:15 for the rework (uuid <LONG_ID>).
- OpusClip API limitation (30.10.): `set_style highlightColor` did NOT change the rendered colour on the 30.10. clips <CLIP_ID> / <CLIP_ID>. The keyword colour stayed green, even after toggling highlight off and on and re-exporting. Some clips are yellow already (Waffles project, bounty). If yellow is needed, the user changes it in the OpusClip editor. User said "alles ok" with green for those two. Cloudinary `e_replace_color` does not work on video.
- Overlays in general (also 9:16 clips): few, short (≤1.2 s), small (short text = small box), never over the action. This replaces the 2-stage hook overlay rule for 16:9 clips.

## PLAYHQ FX VIDEO (user 30.10.: "Das sieht schonmal sehr gut aus"; "Alles andere immer vor den relevanten Postings durchführen sofern passend und überprüfen auf Fehler"; sound: "Punkt 1 lassen" = keep the impact + whoosh)
- **When:** before every relevant post with a strong 16:9 clip (STOP/DON'T/mistake hooks, action; mostly Mon–Wed). Calm menu or tip clips keep the static VIDEO FRAME. OpusClip stays first for clipping and captions; FX are the part OpusClip can't do.
- **Template** `templates/video-fx/`:
  - `fx_overlay.html` – animated PlayHQ overlay:
    - hook slams in with blur + gold flash; logo spins in; edges draw from the centre;
    - corner ticks pulse on punches; gold light sweep over the hook every 3 s; embers; progress bar;
    - bottom band runs through states: question → kill counter → red WANTED stamp → question pulsing at the end.
  - `render_fx.py <src> <out> [fx.json]` does the video part:
    - zoom punch 1.14 + shake 0.35 s on each punch;
    - grade: contrast 1.10, saturation 1.16, mild warm balance (v1 made skies purple – avoid), unsharp, 12 % glow, vignette;
    - 30 fps, crf 16; audio loudnorm −14 LUFS plus a self-made low impact + whoosh on the hook.
- **Per clip:**
  - Set `fx.json` = punches (s), kills (s), wanted [start, end] from scene cuts (`ffmpeg select='gt(scene,0.25)'`) + a 1 fps contact sheet of the captions/keywords.
  - Adapt or remove the clip-specific panels (kill counter, WANTED) in the HTML texts for other topics.
- **Production path** (nothing third-party or account-related in the public repo):
  1. `python3 tools/secure.py "<HD export URL>"` → encrypted `src_url`. Sign the upload with Cloudinary sign-upload (public_id `playhq/work/<slot>_fx`).
  2. `python3 templates/video-fx/make_job.py <name> <enc src_url> <signed.json kept OUTSIDE the repo> [fx.json]` → `fx/jobs/<name>.json` (the upload params are encrypted: they contain account metadata incl. the e-mail).
  3. Push → workflow `fx-render` renders on the runner (~15 min incl. setup) and uploads straight to Cloudinary. Tested 30.10.: 1080×1920, 17 MB.
  4. QA: frames via Cloudinary transformations + fetch-media (12-frame sheet with UI zones, grade, panel timing vs. spoken words, ~−14 LUFS). Delete the frames and the job file afterwards, then schedule the derived URL in Metricool.
  - Local test renders (sandbox) need the source via workflow `grab-private` (draft release asset, download with `gh api -H "Accept: application/octet-stream" repos/<owner>/<repo>/releases/assets/<id>`). Deleting release assets is not permitted from here → tell the user to clean up the draft release "grab-private" occasionally.

## REPO SECURITY (user 30.10.: "Es dürfen keine Rückschlüsse auf unsere IDs oder Accounts etc zu sehen sein. Sonst könnte jemand sensibles stehlen"; repo must stay PUBLIC)
- Never commit account data: e-mail, Metricool blog/brand ID, Cloudinary cloud name/API key/signatures, OpusClip account/project IDs, trigger IDs, post UUIDs, signed CDN URLs (OpusClip/Metricool/Cloudinary).
- URLs for the runner workflows (fetch-media, grab-private, fx-render) are encrypted with `tools/secure.py` (RSA-OAEP + AES with `fx/pubkey.pem`). The private key `fx_key_v2.pem` lives only in the draft release "grab-private"; the runners decrypt with `dec`. Clear `fetch/urls.txt`, `grab/request.txt` and `fx/jobs/*` after use. Workflow logs must not print delivery URLs.
- On 30.10. the brand-assets history was scrubbed (filter-branch) and force-pushed. A force-push re-triggers EVERY path-triggered workflow (music-ai, tts, pixabay, fx-keys…). Avoid it; if unavoidable, check `fx/pubkey.pem` still matches (sha1 prefix 79344cd59461) and restore it if fx-keys regenerated it.
- **Skill backup:** after every skill change run `python3 docs/skill-backup/anonymize.py <SKILL.md> docs/skill-backup/playhq-tiktok-clips.SKILL.md`. It uses generic patterns only, no real values in the script. Check with grep that no ID/e-mail remains, then commit. User: "Speichere regelmäßig deine Skills ab um Verluste zu verhindern" → propose the skill card after every new rule + update the backup.

## Carousel history
- 28.10.: first carousel [PLAYHQ TIP] "5 MW4 DMZ mistakes every beginner makes" (old blurred-screenshot style via Cloudinary transforms) – **2,249 views by 30.10. (97 % FYP), our best recent post** → a "Part 2" carousel ("5 more MW4 DMZ mistakes", verified Waffles tips) was proposed to the user on 30.10.
- 29.10.: [PLAYHQ META] DMZ build carousel (template v3). 10:00 version (9:16, hashtags too narrow) deleted by the user; 11:38 repost (still 9:16 → cut off top/bottom in TikTok) set private by the user; **final 11:52 version: 3:4, uuid <LONG_ID>** (544 views in <1 day), title "[PLAYHQ META] MW4 DMZ loadouts + build codes", cover "UPDATED OCT 2026 / DMZ META / LOADOUTS", tags `#mw4 #mw4dmz #dmz #dmztips #dmzloadout`. User: "Das passt so".
- **Every carousel: `autoAddMusic: true` (user 30.10.: "Bei Karussell immer Metricool anweisen eine gute Musik darunter zu legen").** Music on photo carousels: Metricool only offers autoAddMusic on/off – TikTok picks the sound; no genre/energy control via API (user wish 29.10. "energetische Musik" → not possible).

## META BUILD CAROUSEL – complete procedure (template v3 "digital HUD", approved 29.10.2026)
Use this for every build/loadout/"top X" carousel. Own content → no credit.

### 0. Setup (once per session)
- add_repo owner `PlayHQtv` repo `Claude-Play` access push → clone, `git checkout brand-assets` (work ONLY on this branch, never main). If git complains about tracking: `git config --add remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' && git fetch && git branch -u origin/brand-assets`. The repo is PUBLIC. Rendered test videos are gitignored (`templates/meta-carousel/out/video/`).
- Template: `templates/meta-carousel/` (README, render.py, apex_render.py, icons.py, cutout.py, tiktok_overlay.py, assets/, weapons/, data/, out/). Needs python playwright + chromium (preinstalled), PIL, onnxruntime.
- Sandbox network: GitHub and GitHub release downloads work; res.cloudinary.com, static.metricool.com, signed-ext.cdn.opus.pro, fandom/wikia, PyPI and raw.githubusercontent via curl are BLOCKED. GitHub Actions run logs can't be fetched (403) → workflows write logs into the repo; `gh run list -R PlayHQtv/Claude-Play` shows run status.

### 1. Weapon images (sharpness matters – TikTok likes high-res)
- The user sends screenshots (attachments) or links. For links: add a line `fetch/files/<name>.png <url>` to `fetch/urls.txt`, commit + push to brand-assets → the GitHub Action "fetch-media" downloads it and commits it (~20 s) → `git pull`. Same route for any blocked URL (e.g. Cloudinary AI images, Cloudinary cover checks). Single failed URLs are skipped ("FAILED" in the run), the rest still commit.
- Prefer clean gunsmith/inspect renders ≥1200 px wide on a dark background. Blurry/small sources look soft next to sharp ones → ask the user for a better image (29.10. Kastov: wiki "Kastov_762_Gunsmith_MWII.png" fixed it; tell the user when a render is from an older game or shows the base weapon without attachments). All 28 MW4 gunsmith renders are already cut out in `weapons/mw4/` (see LIST CAROUSEL).
- Cut out: `python3 cutout.py <raw.png> weapons/<name>.png` (ISNet model auto-downloads from GitHub into models/, gitignored). Check the cutout on a dark background.

### 2. Research the builds (ACCURACY RULE – user 29.10.: "Überprüfe die Richtigkeit immer bevor du mir eine Vorschau gibst. Eine fehlerhafte Folie hochzuladen wäre katastrophal")
- NEVER take attachment names from old slides, PDFs or memory (the user-made 29.10. carousel had invented names like "APEX UNDERBARREL", "ZLR REVERB90", "TZL-110 V1").
- Source of truth: codmunity.gg – DMZ: `/best-loadouts/mw4-dmz/long-range` and `/close-range` (pick rates, build codes, "Last Updated"); MP: `/weapon/mw4/<weapon>`. Cross-check names on warzoneloadout.games / wzstats.gg. Record source + date in the data JSON (`source`). If WebFetch is blocked for a site, use the Parallel Search connector (web_search / web_fetch).
- MW4 Apex attachments do NOT use one of the 5 slots (official) → `apex` field = extra gold tile.
- Only claims the data backs: "#1/#2 long range pick" only if the pick-rate order says so; otherwise `rank_label: "BUILD"`, no "Top X", no "BEST" on the cover. Cover kicker "UPDATED <MON YYYY>".

### 3. Data JSON (`data/<YYYY-MM-DD>-<topic>.json`, copy the last one)
- Top level: `game`, `badge` (DMZ), `rank_label`, `cover{kicker,big,small,swipe}`, `cta{white,gold,sub,follow_sub}`, `source`, `notes`.
- `weapons[]` in slide order: `rank, image, short, title_white, title_gold, class, class_note ("DMZ Loadout"), tagline, brightness (1.1–1.45), build_code, apex?, attachments[{type,label,name}]` (max 5).
- Names UPPERCASE, spelled exactly as the source. Icon types: barrel, muzzle, optic, underbarrel, reargrip, stock, magazine, drum (drum mags), ammo, apex, laser, comb – a new type → add it to icons.py (gold HUD line style) and run `python3 icons.py`.

### 4. Render
- `python3 render.py data/<file>.json` → `out/<file>/01_cover.jpg … NN_cta.jpg` at **1080×1440 (3:4)** – the format TikTok actually shows for photo posts (9:16 gets cropped). Rendered at 2× and downsampled, light unsharp, JPEG q95 without chroma subsampling (~550 KB each).
- TikTok-safe layout built into the template: header row (CALL OF DUTY · MW4 + DMZ badge, logo 96 px at right:170) at y≈120–170 below the search bar/tabs; titles max 850 px wide (clear of the "2/6" counter); grid/hdr/cards/rows end at x≈935 (right button column starts x≈940 from y≈1100); all content ends by y≈1260 (first-comment bubble y≈1320+); no footer on weapon slides.
- Design v3 (keep it, don't restyle): black background with gold topo lines, warm glow and diagonal gold streaks, thin gold corner brackets; weapon title in Anton with grunge texture (white word + gold word, one line ≤10 chars else two lines, auto-fit); spaced Rajdhani tagline; "BUILD #n"; weapon on a gold glow/floor line; "ATTACHMENTS" HUD bar with BUILD CODE; 2×3 HUD tiles (angled corners, scanlines, yellow tick, index 01–05, glowing gold line icon in a grid box); 6th tile gold "SAVE THIS BUILD" (or the gold APEX tile).
- Cover: kicker, big gold + white title, 2×2 weapon cards, swipe line. CTA: two-line question, numbered rows with weapon images, logo + clean "FOLLOW <OUR_TIKTOK_HANDLE>" (no grunge on small text – it becomes unreadable).
- User REJECTED: glass/glassmorphism look, cut-out real part photos as icons, simple filled icons ("billig"), the game-icons.net set, gold-statue duotone parts. Cloudinary AI images cost 9 of 50 monthly credits each (premium model) – only with the user's OK.

### 5. Verify BEFORE showing anything
1. `python3 tiktok_overlay.py out/<name>` → `_qa/*.jpg` + `_qa/sheet.jpg` with the TikTok UI zones in red (measured from the user's screenshot 29.10.). Read the sheet and full-size slides: no text/weapon/tile inside a red zone, no overlaps, no clipping, long names (≤16 chars one line, longer ones wrap).
2. Independent verifier agent (general-purpose, foreground): it re-fetches the sources itself (or gets the verified values), compares every name/slot/build code/rank/claim character by character with the slides, checks the `_qa` versions for UI collisions and gives a PASS/FAIL verdict. Fix everything and re-check.
3. Commit + push template/data/out to brand-assets.

### 6. Preview for the user
- Artifact page with the slides embedded as data URIs (the artifact CSP blocks external images), horizontal swipe track, 720×960 previews; optionally send one `_qa` slide so the user sees the safe zones. Say what was verified and with which source.

### 7. Publish (only after the user's OK; never overwrite a user-made post without an explicit OK)
- Cloudinary upload-asset per slide from `https://raw.githubusercontent.com/PlayHQtv/Claude-Play/<full commit SHA>/templates/meta-carousel/out/<name>/NN_x.jpg` (use the SHA, not the branch name, to avoid a stale cache), public_id `playhq/carousel/<date-topic>/NN_x`. Byte sizes must match the local files.
- Metricool create/updateScheduledPost at a POSTING TIMES slot (12:00 or 18:00): media = the secure_urls in slide order; tiktokData `{title:"[PLAYHQ META] …", autoAddMusic:true, photoCoverIndex:0, privacyOption:"PUBLIC_TO_EVERYONE"}`, autoPublish true.
- Caption: "[PLAYHQ META] MW4 DMZ loadouts …" (search phrase first), weapons in slide order, build code + save CTA, question. **Hashtags: `#mw4 #mw4dmz #dmz #dmztips #dmzloadout`** (NOT #mw4builds/#codmeta/#mw4meta – too narrow). First comment: question with keywords ("Which MW4 DMZ build is your main: 1, 2, 3 or 4?").
- Check: upload 2 of the returned static.metricool.com URLs back to Cloudinary `playhq/tmp/…` → the etag must equal the originals (Metricool stores byte-identical copies), then delete the tmp assets.

### LIST CAROUSEL variant: "EVERY APEX IN MW4" (30.10., uuid <LONG_ID>, Sat 31.10. 12:00)
- Template: `apex_render.py` + `data/2026-10-30-mw4-every-apex.json` (items: n, weapon, apex, cls, level, effect, image). Slides: cover, 7 list slides × 4 HUD cards (image, `NN/28 WEAPON · CLASS`, gold apex name, `MAX LVL`, 1-line effect), CTA ("WHICH APEX IS THE BEST?" + SAVE THIS + follow). Reusable for any "every X" list. Hashtags `#mw4 #mw4dmz #dmz #dmztips #mw4apex`.
- **Data source for MW4 weapons and Apex (official):** callofduty.com blog "Ready for Launch: All MW4 Operators, Weapons, Equipment…" (19.10.2026). It gives exactly 28 Apex at launch (one per weapon; launchers and the knife have none) and Levels = weapon levels to max = Apex unlock. Extracted copy: `data/2026-10-30-apex-official-source.json`. Check the patch notes for renames (29.10.: none; beta-only event Apex "will return soon").
  - Official spellings: Signal Inferno, SANG Breach, GS Magna, Mojave Lawless, Mosin Harpoon, WZ.55 Striga Rampage, KG-7 Drillcharge.
  - Axion: the official blog says "Axion Clearcut"; the Steam copy and 3rd parties say "Axion Reaver" → the slide says "Clearcut (aka Axion Reaver)" until the user checks in game.
- Spelling / existence check: `data/mw4-weapons-reference.md` (wiki navbox, user screenshots 30.10.).
- **High-res MW4 weapon renders (free):** Call of Duty Wiki "<Weapon> Gunsmith MW4.png"; some Apex renders exist as "<Apex> Apex Gunsmith MW4.png" (Han X20, Rezi Enforcer, Krait Commando).
  - Fandom pages and api.php are blocked for curl/GitHub, but the Parallel Search web_fetch can read api.php (e.g. `list=search&srnamespace=6&srsearch=Gunsmith MW4`).
  - Image URL = `https://static.wikia.nocookie.net/callofduty/images/{md5[0]}/{md5[0:2]}/{File_Name_with_underscores}/revision/latest` (md5 of the filename) → fetch-media.
  - Files are WebP despite .png.
  - All 28 base renders are cut out with ISNet in `weapons/mw4/` (w_*.png, a_*.png). The Krait Commando Apex cutout failed, so the base Krait is used. The Striga cutout was cleaned manually.
- Showcase VIDEO variant (`apex_video.py`, 2.5D turn + light sweep + gold wipe) was tested 30.10. User: "Vergiss es" → don't offer it again unless asked.

## NARRATED VIDEO route – PARKED (user 29.10.: "Merke dir für später mal diese Route mit Pixabay, Voice usw. Wir brauchen es jetzt noch nicht") – only use when the user asks
Turns carousel slides (or other stills) into a 9:16 video with a free AI voice, uppercase captions and quiet background music. Videos >60 s count for Creator Rewards. Never post without the user's OK. (Slides are now 3:4 → pad/extend to 9:16 for video and keep captions out of the right button column.)
1. **Voice (Kokoro, Apache-2.0, free):** GitHub Action `tts` (`.github/workflows/tts.yml`). Write `tts/jobs/<job>.json` = `{"voice":"am_michael","speed":1.08,"lang":"en-us","segments":[{"id":"<slide file name>","text":"..."}]}` → commit + push to brand-assets → ~1 min later `tts/out/<job>/<id>.wav` → `git pull`. (PyPI is blocked in the sandbox, so TTS runs on GitHub.) Script = only verified facts; write numbers/names the way they should be spoken ("sixty round drum", "Gauge 12 Mono"). Example job: `tts/jobs/2026-10-29-dmz4.json` (64 s for 6 slides).
2. **Video:** per slide duration = wav length + 0.45 s; ffmpeg zoompan slow zoom (1 → 1.035, 30 fps, from a 2× upscaled still), concat. Captions as ASS: Rajdhani Bold 78, yellow `&H0000D4FF`, black outline 5, 3-word chunks timed proportionally to characters, **UPPERCASE** (user 29.10.), `\pos(540,y)`; libass `fontsdir` = template assets/fonts; x264 crf 17, faststart.
3. **Music:** my procedural synth beat was rejected ("klingt Scheisse") – don't use it. Use **Pixabay Music** (free, commercial use OK, no attribution). Pixabay blocks automated downloads (also from GitHub Actions) → the user downloads the MP3 and attaches it. Approved test track: Paul Yudin "Action" (pixabay <ID>, 2:34, -11 LUFS), start at 6 s to skip the quiet intro. Mix: music volume 0.13, `sidechaincompress` ducking under the voice (threshold 0.03, ratio 5, attack 20, release 400), fade in 0.8 s / out 2.5 s, final `loudnorm I=-14:TP=-1.5:LRA=11`. Some Pixabay tracks are Content-ID registered → user checks the track page. I can't listen to audio myself – the user judges music.
4. **AI music (Suno-like, free):** ACE-Step 1.5 (MIT) via GitHub Action `music-ai` (`music/jobs/<job>.json` = `{"caption","duration","bpm","count"}` → `music/out/<job>/*.flac`, logs in `music/logs/`), CPU runner, installed with the official `uv sync`, `thinking=False`, turbo model. **Works (29.10.):** 2 × 70 s "dark energetic phonk trap" tracks in ~14 min, -14/-16 LUFS. User hasn't judged them yet. Stable Audio Open Small is an alternative (free under $1M revenue, needs a free Hugging Face account).
5. **Own voice later (free, commercial OK):** Chatterbox (Resemble AI, MIT) or OpenVoice v2 (MIT) – need PyTorch → run via GitHub Actions. Only the user's own voice or with explicit consent. Captions from real speech: faster-whisper.

## FREE TOOLBOX (user 29.10.: "Füge die anderen zu deiner Datenbank hinzu") – details in `TOOLS.md` in the repo (branch brand-assets)
All open source or free without account/trial. Set up a tool only when a task needs it or the user asks; heavy ones run as GitHub Actions (PyTorch is not available in the sandbox).
- **In use:** ISNet cutout, Playwright + ffmpeg, Kokoro TTS, ACE-Step music, fetch-media, PlayHQ video frame (Playwright + Cloudinary overlay), PlayHQ FX video (fx-render workflow).
- **Priority (user 30.10.: "Nutze die Tools nur wenn Opus es nicht schafft"):** OpusClip first; GitHub tools only when OpusClip can't (FX, captions colour, upscaling <1080p, sound check). Candidates in TOOLS.md: karaoke-subs, RIFE, Video2X, earshot (later).
- **Ready to set up when useful:**
  - **Demucs** (MIT): split voice / game sound / music → remove copyrighted music from source clips (fewer mutes), cleaner creator voice.
  - **faster-whisper / WhisperX** (MIT/BSD): word-accurate captions from real speech in PlayHQ style, independent of OpusClip.
  - **Real-ESRGAN** (BSD-3): AI upscaling of blurry weapon renders / stills to 1080p+ (quality rule 7).
  - **auto-editor** (Unlicense): gentle silence/idle cutting – alternative to OpusClip remove_pauses, which breaks gameplay clips.
- **Noted only:** PySceneDetect (BSD-3, finds scene changes/action moments) – user 29.10.: "nur im Gedächtnis behalten, da wir dafür schon OpusClip haben".
- **Later:** Chatterbox / OpenVoice v2 (own voice), Remotion (animated templates, free for individuals/teams ≤3), Piper (fast TTS incl. German).
- **MCP connector:** Parallel Search (free, no login; web_search / web_fetch) – connected 29.10., use for research when WebFetch is blocked. Registry check 30.10.: no other useful free connector (TikTok for Business/AdWhispr/Adspirer = paid ads, Supermetrics paid, vidIQ excluded, no CapCut).
- **Free in-app data the user can screenshot:** TikTok Studio (retention curve, search terms) and Creator Search Insights (content gaps).
- **Avoid:** non-commercial models (XTTS-v2, F5-TTS, MusicGen, Suno free tier); paid/trial tools (ElevenLabs, JsonCut beyond its free quota – checked 29.10., proprietary freemium with token limit, we do the same with ffmpeg; Semrush, TinyFish, Orshot, Riverside, Tella); vidIQ; anything needing a Google account; unofficial TikTok scrapers (account risk); downloaders for other people's videos without permission.

## PlayHQ logo (29.10.): Design "B – Play-Button" (middle draft from 13.10., artifact "PlayHQ Logo-Entwürfe"): black circle, dashed yellow ring, yellow play triangle, "PLAY" white + "HQ" yellow (Russo One). Stored permanently in Cloudinary as `playhq/brand/logo` = 1024×1024 transparent PNG (DON'T delete, not a tmp asset). Master copy in GitHub repo PlayHQtv/Claude-Play, branch `brand-assets`, file `brand/playhq-logo.png` (re-upload from raw URL if ever lost). Any size works, no `r_max` needed (corners transparent), e.g. `l_playhq:brand:logo/c_scale,w_140/fl_layer_apply,g_north_east,x_50,y_270` (keep inside safe zone y≥260) or big on carousel outro slides. Carousel slides (3:4): round logo 96 px at right:170, top 118 (left of the TikTok counter).

## OWN CONTENT rule (user 29.10.): content PlayHQ made itself (e.g. the "[PLAYHQ META]" build carousels) needs NO credit. The credit rule applies only to clips/material from other creators.

## User-made posts (29.10.)
- The user (or another session of his) also creates posts himself in Metricool (e.g. the first META carousel uuid <LONG_ID>). Never overwrite posts I didn't create; ask first. Before planning a day, check getScheduledPosts for user-made posts and plan around them. The user also deletes/privates posts on TikTok himself when something is wrong.
- Plan as of 30.10.:
  - Fri 30.10.: 10:00 "Pay to win?" (posted); 18:00 SiNister "Fight or skip?" (uuid <LONG_ID>).
  - Sat 31.10.: 12:00 Every Apex carousel (uuid <LONG_ID>); 18:00 Waffles bank upgrade (<CLIP_ID>, uuid <LONG_ID>).
  - Sun 01.11.: 12:00 Waffles survival kits (copy <CLIP_ID>, uuid <LONG_ID>); 18:00 open.

## Compilations – CANCELLED (user 28.10.: "das Video ist scheisse, streiche die Idee")
- Tested a Cloudinary fl_splice compilation "3 MW4 DMZ survival tips" from 3 creators → rejected. Don't build multi-clip compilations again unless the user asks. The 3 edited segment clips (<CLIP_ID>, <CLIP_ID>, <CLIP_ID>) are too short to post alone.

## 9:16 format (user 28.10.) – ON HOLD (OpusClip auto-reframe only; the PLAYHQ VIDEO FRAME above is the approved way to deliver 16:9 clips as 9:16): user said "Lasse das erstmal …, das werde ich dann selbst mal prüfen" → keep the current formats, no 9:16 re-submits until the user says otherwise.
- Tips with menus/UI text stay 16:9 (readable). Action/fun sources (from November) may be submitted in 9:16 with OpusClip auto-reframe (aspect is fixed at submit, costs credits).
- RULE: before using any 9:16/reframed clip ALWAYS check that the subject is centered and nothing important is cut off (kill feed, minimap, text, the action itself). I can't view frames myself → check OpusClip layout info in describe_clip and send the user the preview link to confirm; if in doubt, keep 16:9.

## HASHTAGS v3 (user 28.10.: "Pass auf die richtigen Hashtags auf! Zu breit ist nicht gut") – overrides scheme v2 and the series tags
- NO broad tags anymore: no #gaming, #gamingontiktok, #gamingtips, #funnygaming, #callofduty (too broad). Series is shown via "[PLAYHQ TIP]/[PLAYHQ FUN]/[PLAYHQ META]" in title/description instead.
- But not too narrow either (user 29.10.: "viel zu eng"): always include the mode tags. 5 tags = game + game-mode combo + mode + mode-tips + specific topic. MW4 DMZ default: `#mw4 #mw4dmz #dmz #dmztips #<topic>` (topic e.g. #dmzbounty, #dmzkeys, #dmzbeginner, #mw4blueprints, #dmzexfil, #dmzpvp, #dmzloadout, #dmzstash, #mw4apex). Other games the same way, e.g. CS: `#cs2 #counterstrike #csgo #cursedweapons #cs2funny`.

## GOAL (user 28.10.): ~50,000 views in ~2 weeks (28.10.–11.11.2026) ≈ 3,600/day (baseline ~900–1,500/day)
- Needs 1–3 breakouts (5–20K). Use only the strongest clips (highest hook scores first: MrMarvel <CLIP_ID> "10 things to do first", bounty "lobby hunts you", SiNister "when to fight a squad"), one polarizing STOP/mistake/DON'T hook per day, immediate "Part 2" within 1–2 days when a post passes ~1,500 views in 24 h, more carousels (they work). User: pin first comment + reply in the first hour. No re-uploads of old videos, max 2 posts/day (POSTING TIMES).
- Daily report must include goal tracker: views since 28.10. (sum TKEV02), remaining, on/off pace. 28.10. = 2,722, 29.10. = 926 (Metricool, updated 30.10.) → 3,648 total; clearly behind pace.

## FOCUS DECISION (user 28.10.: "dann machen wir es so vorerst"; no new sources until November)
- ~80 % MW4 DMZ, ~20 % other games (CS cursed, Asmongold …). Per week of 14 posts: ~11 MW4 (tips, carousels, PvP/action-type tips in the evening) + ~3 FUN from other games. After ~30 posts rank clip types by completion rate.
- MW4 inventory in OpusClip (unused, 30.10.):
  - MrMarvelTV <OPUSCLIP_PROJECT_ID>: <CLIP_ID> "10 things to do first" (score 99, hook 9; intro teaser only), <CLIP_ID> AI threat level/escalation, <CLIP_ID> extraction ambushes + Fulton, <CLIP_ID> 13 POIs ranked by threat (calls map "Hazan" – say Hajin in text), <CLIP_ID> 3D printer backpack, <CLIP_ID> progression lvl 2–70, <CLIP_ID> operator trait trees, <CLIP_ID> 3 ways to play, <CLIP_ID> operator prestige, <CLIP_ID> stealth + FOB, <CLIP_ID>/<CLIP_ID>/<CLIP_ID> (weaker). Used: bounty <CLIP_ID> (29.10.), gunsmith pay-to-win <CLIP_ID> (30.10.). MrMarvel clips are landscape 16:9 → use the PLAYHQ VIDEO FRAME.
  - SiNisterFPS <OPUSCLIP_PROJECT_ID>: <CLIP_ID> solo looting mistake (87), <CLIP_ID> when to fight a squad (position/ammo/armor/escape – good follow-up to the fight post), <CLIP_ID>/<CLIP_ID> spawn locations, <CLIP_ID> PvPvE awareness, <CLIP_ID> audio cues, <CLIP_ID>/CBPM191IKU secure-slot backpack, <CLIP_ID> free loadouts, <CLIP_ID> 3D printer, <CLIP_ID> loot early, <CLIP_ID>, <CLIP_ID>, <CLIP_ID>. Used: <CLIP_ID> → copy <CLIP_ID>. Reserve edited: <CLIP_ID> "stop fighting the AI". (Some are pre-launch info – check facts.) OpusClip previews of this project have burned-in captions → crop cover stills.
  - Waffles <OPUSCLIP_PROJECT_ID> (clips have uppercase yellow captions built in): left <CLIP_ID>, <CLIP_ID>, <CLIP_ID>/<CLIP_ID>, <CLIP_ID> (cancel dynamic ops + zoom map), <CLIP_ID>, <CLIP_ID>, <CLIP_ID>, <CLIP_ID>, <CLIP_ID>. Used 30.10.: bank <CLIP_ID>, survival kits <CLIP_ID> → <CLIP_ID>. Skip <CLIP_ID> Sky Heist (the promised tip is cut off).
  - No MW4 DMZ fun/clutch sources (reload-fails project already posted 08.10.; weapon inspect project weak; LegoUnlocked cancelled by user).
- Rotate creators daily (Waffles / SiNister / MrMarvel) so clips don't feel repetitive.

## ACCOUNT FORMAT (user 28.10.: "Tipps und Tricks zu Spielen + ein bisschen Spaßvideos") – two fixed series, every post belongs to one
- **PLAYHQ TIP** (main, 12:00 daily): tips & tricks/mechanics/mistakes for a game (MW4 DMZ now). Title/description start: "[PLAYHQ TIP] <Game>: <tip>". Cover label: "PLAYHQ TIP · <GAME>". End overlay "PLAYHQ 9/10" + question.
- **PLAYHQ FUN** (18:00 daily): funny/cursed/streamer moments (CS cursed weapons, Asmongold …). Title/description start: "[PLAYHQ FUN] <Game>: <story>". Cover label: "PLAYHQ FUN · <GAME>". End "PLAYHQ x/10" + "Rate it 1-10?".
- **PLAYHQ META**: build/loadout/list carousels (procedures above).
- Hashtags: see HASHTAGS v3.
- Same structure every time so TikTok recognizes the account by format, not by game. Ratio ~2/3 tips, 1/3 fun is also fine if tips perform better.

## TikTok's own creator guidance (user screenshots 28.10., keep in mind for every post)
**More views:** (1) Hook in the first 3 s – exciting moment, cliffhanger question or punchy title (TikTok example: not "My gameplay" but "[PENTAKILL] How I beat the enemy team 1 vs 5!"). (2) Pleasant to watch/listen: stable, well-lit picture, clean noise-free audio; face cam, simple subtitles or background music make it more dynamic. (3) Real added value – don't just post raw gameplay snippets: add useful insights, stories or a personal view; solve problems (explain mechanics, tutorials), share knowledge (meta, news), tell stories (comebacks, challenges).
**More followers:** (1) Stick to ONE niche and post regularly – same game OR one content type (e.g. tutorials), so TikTok can recommend to likely followers. Examples TikTok gives: funny Fortnite fail compilations, CS:GO highlight montages. (2) Interact: answer comments quickly, ask questions in videos, make content from viewer suggestions.
→ Implications: keep a recognizable PlayHQ format across games (hook + PlayHQ verdict/rating + question = "PlayHQ rates it"), prefer clips with face cam + clean audio, always add our own view (verdict, insight), make "reply to comment" videos when good comments come in, user should answer comments in the first hours.

## TikTok handbook learnings (marketingexamined.com/blog/tiktok-handbook, user 28.10.)
- Watch time/completion is king (a 2M video had 95 % completion) → one tip per video must stay short; long only if fast-paced with story.
- Hook = first 1.5 s (aesthetic, sound, drama, humor, shock); show the payoff visual in second 1 AND on the cover.
- Headlines like ad copy for a "micro view": data, reason, test, hint, experience, question, straight talk, problem→solution.
- Native on-screen text supports the story; study viral niche videos and copy their text style.
- Trending sounds should amplify value, not replace it; relevant trending hashtags can reach Discover.
- Engagement: reply to and PIN best comments, make "reply to comment" videos, comment-driven loops (answer hidden in comments) increase replays.
- Formats that work: numbered SERIES (Part 1/2/3 → profile visits), reactions, quick tips, reviews, news, duets/stitches on viral videos, single recurring voice/personality.
- Test 2–3 weeks, then scale the winning format. Avoid salesy CTAs and copying content without making it native (always add our own framing).
→ Ideas to apply: numbered "PLAYHQ TIP #n" series, "Part 2" follow-ups to winners, pin first comment (user), reply-to-comment videos.

## Eklipse gaming-algorithm notes (blog.eklipse.gg tiktok-algorithm-gaming-creators, user 28.10.; vendor source)
- Seed test: 200–500 accounts in the first 1–3 h; completion rate is the top signal (~30–40 % completion → wider push to 2–10K); then likes, shares/saves, comments.
- Game name in hashtags AND first caption line so TikTok puts the clip into the right game interest pool. 3–6 hashtags (game + moment type, e.g. #clutch); #fyp/#viral useless.
- Gameplay clips: cut straight to the moment, no lobby/menu/setup; clutches start ~3 s before the first fight; open with action in motion, one text hook or a reaction; 15–30 s (max 45). Keep the kill feed / outcome readable for non-players.
- Post consistently (5–7/week minimum, no bursts+gaps). Avoid repetitive low-effort clips. (Our own times: POSTING TIMES.)
- If completion stays <25 % → fix length/hook; reach stuck at seed → hook or mid-clip retention problem.
→ Our check: menu-heavy Waffles clips break the "no menus" rule → prefer in-game action frames in second 1.

## Eklipse "grow gaming TikTok to 100K" (user 28.10.; vendor source, partly unsourced claims)
- Stay in ONE game ~90 days; add a 2nd game only after 10K followers and max 20 % of posts (switching games makes TikTok relearn + followers disengage). → conflicts with "all games"; discussed with user.
- At ~30 posts rank clip types by COMPLETION rate (not views) and drop the weak types (example: clutches 35 % vs montages 12 % → clutch-only 800→8.2K in 6 weeks). Video <20 % completion = diagnostic.
- Reply to every comment within the first hour, ask follow-up questions.
- At 10K: duets/stitches with 20–100K creators of the same game. Trending sounds mainly later (50K+), only if energy fits.
- Cadence: 0–10K 1 post/day (we do 2 – fine, but quality > quantity); 10–50K 1–2/day.
- Benchmarks: 10K in 45–90 days with daily posts in one niche; 100K in 6–12 months.

## Cover SAFE ZONE (checked on profile grid 28.10.): custom covers DO show (personal account works). Profile grid crops ~3:4 and the view counter covers the bottom of the tile → ALL text must sit between y≈260 and y≈1350 of the 1920 canvas (labels at y_280, main text y_390–620, frame below at g_north y_720–760). Never put text at y>1350 (Door Stuck "AS A GUN?" and Knife "KNIFE?!" were hidden behind the counter). For 3:4 carousel covers the grid shows the whole image; keep text above ~1260 (view counter).

## Cover VARIETY rule (user 26.10.): every cover must look different – rotate layouts, never the same layout twice in a row; vary colors/positions/fonts per post. Layouts:
- **A "Classic"** (below): red label top, yellow line 1 + white line 2 above the frame, frame center.
- **B "Bottom punch"**: frame at top (`c_scale,w_1000/bo_8px_solid_white/fl_layer_apply,g_north,y_250`), black label with yellow text at y_150, big black-on-yellow box line 1 tilted `a_-4` at y_1280, white stroke line 2 at y_1460 (used 26.10. CS Door Stuck).
- **C "Center band"**: blue label `b_rgb:1e90ff` at y_290, line 1 white on a black band (`b_black`, text padded with spaces) at y_410, line 2 yellow stroke at y_560, frame center y_120.
- **D "Big word"**: one huge word (Arial 200+, e.g. "STOP", "WHAT?!") in yellow tilted a_5 overlapping the top of the frame, small white subline.
- **E "PlayHQ frame"** (29.10.): the video-frame composite still (`so_<sec>` at a payoff moment) – used automatically for 16:9 clips with the PLAYHQ VIDEO FRAME.
- Also vary label color (red/black/yellow/blue rgb:1e90ff), border color and brightness. Square (1:1) frames: scale w_900–1000 so the text doesn't overlap.
- OpusClip previews can contain burned-in captions (SiNister project): crop them away with `c_crop,g_north,h_300,w_720` on BOTH the background and the layer (else the blurred background still shows the caption).

## Cover – approved style (20.10.2026)
Full 16:9 frame uncropped in the middle, blurred version of the same frame as background, hook text in the safe zone (TikTok profile grid crops ~3:4 center; UI on right/bottom). On the FYP TikTok shows the video, not the cover.
1. Upload the ORIGINAL clip HD export (no captions) as video (720p preview only as a last resort, then upscale): public_id `playhq/tmp/<YYYYMMDD>-slotX`.
2. Upload a still as image: file `https://res.cloudinary.com/<CLOUDINARY_CLOUD>/video/upload/so_<SEK>/f_jpg/q_auto:best/v<version>/playhq/tmp/<YYYYMMDD>-slotX.jpg` → public_id `playhq/tmp/<YYYYMMDD>-slotX-still`. SEK = the scene the video is about.
3. `transform-asset` (image) on the still:
   `c_fill,h_1920,w_1080/e_blur:1500/e_brightness:-45/l_playhq:tmp:<YYYYMMDD>-slotX-still/c_scale,w_1040/e_sharpen:80/bo_6px_solid_rgb:ffd400/fl_layer_apply,g_center,y_130/b_rgb:e10600,co_white,l_text:Arial_70_bold:%20MW4%20DMZ%20/fl_layer_apply,g_north,y_320/bo_10px_solid_black,co_rgb:ffd400,l_text:Arial_118_bold_stroke:<LINE1>/fl_layer_apply,g_north,y_430/bo_10px_solid_black,co_white,l_text:Arial_118_bold_stroke:<LINE2>/fl_layer_apply,g_north,y_575/f_jpg/q_auto`
   - LINE1/LINE2 = video hook, ≤ ~13 chars each, caps. Result width must be 1080 (else font 105). Red label can say "MW4 DMZ PART 2" etc.
   - Encoding: space `%20`, `?` `%253F`, `#` `%2523`, `,` `%252C`, `/` `%252F`, `'` `%27`, `·` `%C2%B7`; avoid `+`. Custom Google font names fail in Cloudinary text layers ("Unknown text style") – use Arial.
4. **Check the cover visually** (fetch the eager URL via the GitHub fetch-media workflow, then Read it). Metricool `videoThumbnailUrl` = eager secure_url; after Metricool stored it, delete both Cloudinary assets (`delete-asset` needs its params wrapped in a `request` object).
- Always take stills from the OpusClip HD export (quality rule). 20–35 s HD exports are 17–48 MB, fine for Cloudinary (100 MB limit). If an export is >100 MB, upload with `async: true` or trim it. Cloudinary sometimes reports "partial download" for a fresh OpusClip export → retry with `async: true` (works). Only fall back to the 720p preview if nothing else works, and then upscale the still to 1080 wide (rule 7).
- Fallback if Cloudinary fails for any reason: `videoCoverMilliseconds: 1000` and mention it in the report.

## Posting pipeline
0. **ALWAYS first: full data check (user rule 24.10.: "Beachte immer sämtliche Daten bevor du etwas postest. Du sollst von selbst immer besser werden").** Pull TKPO02/05/06/07/08/09/10/11/13/15/16/21 for all posts + TKEV02/07 + getBestTimeToPostByNetwork. Compare: which topic, hook type, length, weekday and slot got the best avg watch time, full-watch rate, shares and FYP/search share. Derive what to change for THIS post (topic choice, hook wording, length, slot) and note learnings in "What the data taught us". Report the key takeaway briefly to the user.
1. OpusClip: list_clips → describe_clip (transcript: clean? creator clear? strongest line? `aspect` landscape → PLAYHQ VIDEO FRAME) → duplicate_clip ("(Copy)" = used).
2. edit_clip: delete_phrase for intros/outros (adjacent phrases in one delete), reorder if needed, remove_filler_words, remove_pauses, set_captions true, set_emoji false, style/highlight; then overlays (2-stage hook / mid open loop / verdict – for 16:9 clips none, the frame carries the text). If an edit says "dropped stale overlay sections", re-check overlays with dryRun and re-add.
3. export_clip hd → poll until ready (wait ~35–45 s with a bash timeout loop). Make sure the export is newer than the last edit.
4. Cover. 5. Run the checklist + PRE-PUBLISH GATE. 6. Metricool createScheduledPost at 12:00 or 18:00 (tiktok, Europe/Berlin, tiktokData.title required, PUBLIC_TO_EVERYONE, autoPublish true). To change: updateScheduledPost with full content (id changes, uuid stays). Media can be reused via its static.metricool.com URL. To publish "now", set publicationDate ~2–3 min in the future. Publishing takes a few minutes (PUBLISHING → AWAITING_CONFIRMATION → PUBLISHED) – normal.

## Analytics
- Posts: TKPO02 time (**UTC** → +1 h winter from 25.10. / +2 h summer for Berlin), TKPO05 text, TKPO06 duration, TKPO07 views, TKPO08 likes, TKPO09 comments, TKPO10 shares. Values come in requested order. Metricool refreshes ~daily and lags (a post showed 291 while TikTok had 4,087).
- **Insight metrics work since 23.10.** (also retroactively): TKPO11 reach, TKPO13 full-watch rate, TKPO15 avg watch (s), TKPO16 For-You share, TKPO21 search share. Metricool refreshes ~daily, so same-day posts appear the next day.
- Learnings 30.10.: "5 mistakes" carousel 2,249 views (best recent post); META carousel 544 in <1 day; first framed video (bounty) 382 views overnight with 11 s of 21 s avg watch (52 %, good). Followers 156.
- Learnings 29.10.: carousel "5 mistakes" 623 views/<1 day (95 % FYP) > Keys video 411; "What happens when you die" grew 568→724; "Don't buy this gun" 1,207; traits 1,107.
- Learnings 28.10.: MW4 beats CS clearly: Mon "Don't buy this gun" 1,171 (12 s/20 s = 60 %) & Tue "You died" 568 (13 s/31 s) vs CS "Door Stuck" 424 and "Silenced Knife" 245 → CS fun underperforms; supports 80/20 focus. OpusClip sometimes adds its own auto-hook overlay to copies (e.g. "DMZ Blueprints May Skip the Grind") → always check the overlay list and remove it. Skipped: <CLIP_ID> "10 things" is only an intro teaser (no payoff, mentions early access) and <CLIP_ID> duplicates the posted "STOP this body" topic.
- Learnings 27.10.: "Don't buy this gun" (Mon 10:00, small verdict, DON'T hook, 20 s) = 1,067 views in <1 day, avg watch 12 s (60 % – best ratio so far), 99 % FYP. CS "Door Stuck" (Mon 18:00, 30 s) 412 views after ~14 h, avg 14 s, 6 comments ("Rate it 1-10" drives comments). New posts start ~100 % FYP; search share builds over days. Sunday posts kept growing (traits 436→720).
- OpusClip gotcha: never run two edit_clip calls on the same clip in parallel / right after each other with other calls in between – one edit got silently lost (timeline_before reset). Always check timeline_before/after and overlay list; export only after the last edit returned.
- Learnings 26.10.: Waffles tip clips land at ~440–570 views in the first days (weekend ≈ weekday), but keep growing via search (25–42 % search share; "Free legendary" 780→1,124, knife 420→568 within 3 days) → evergreen SEO value. Breakouts (5.1K, 1.6K, 1.1K, 0.9K) all had "STOP / mistake / lose your loot" hooks + polarizing topic → keep 1 such hook per day in the 12:00 slot Mon–Wed.
- Learnings 24.10.: weekends ~40 % less audience activity; hits came Mon/Tue; 29–30 s clips beat 18–19 s edits on avg watch and views; info topics get 30–45 % of views via search.
- Learnings 13.10. (early CS phase): "Cursed Weapon of the Day" series and crazy-weapon CS clips worked best then; GTA 6 news and streamer humor were weak; 4 posts/day cannibalized.
- Account: TKEV02 views, TKEV07 followers, TKEV08 new followers, TKEV09 profile views.

## Known limits
- No connector for TikTok organic stats/Studio or YouTube search (except vidIQ, excluded); Claude in Chrome (user's Chrome open with extension) is the way. TikTok/YouTube pages can't be fetched directly.
- OpusClip: no music, no custom cover, no background/frame design, aspect ratio fixed after submit; TikTok links not supported. Text overlays are always a white box with black text (only text/position/timing editable). Highlight colour via API unreliable (see VIDEO FRAME). OpusClip schedule_publish / create_post_task need manual approval in the OpusClip app → use Metricool.
- The sandbox can't download from Cloudinary/Metricool/OpusClip CDN/PyPI/most websites → use the GitHub workflows (fetch-media, tts, music-ai) or upload the URL straight into Cloudinary. AI upscaling (EDSR via OpenCV 5) doesn't work here; no torch locally.
- No sound choice via API (personal account, but Metricool/OpusClip can't set sounds). Metricool "autoAddMusic" only for photo posts (TikTok picks the sound). User declined manual in-app sound posting (28.10.).
- Can't edit published TikToks, reply to comments, pin, delete or make posts private – the user does that in the app. No TikTok Stories, no auto-following, no Promote data.
- Metricool TikTok error 401 "did not authorize the scope" = reconnect TikTok in Metricool with publish permission.
- Metricool checkout requires a tax ID field (private persons: Steuer-ID).
- No external links in descriptions. Copyright: reposting is risky; safe sources are CC-BY, creators who allow clipping, own content. TikTok in-app game challenges must be joined in the app.