# Reach log (anonymized)

## 2026-11-24 – view drop analysis
- Early Nov build posts: 4k–12k views, 84–97 % from TikTok search (long keyword captions).
- Since short captions (11.11.): build posts 235–1,100 views, search share down to 20–79 %.
- Other factors: Season 1 launch hype over, GTA 6 launch (19.11.), niche weapons (Axion, Cronen Squall).
- Change: SEO CAPTIONS v2 (long keyword captions) from 25.11. Test window 25.11.–01.12.; compare search share + views at day 3 against 17.–24.11.
- Next test after that: topic choice (high-search meta weapons vs niche).

## 2026-11-25 – early warning run
- ALARM (search share): last 3 posts Rezi 12 34 %, best LMG 40 %, Cronen Squall 36 % search share vs 80–97 % on early-Nov build posts. Views at the same age: Rezi 219 (age 1, worst at age 1), color settings 304 at age 3 = below 50 % of the age-3 median (780).
- Cause (same as 24.11.): short captions (11.11.–24.11.) + niche guns/topics with low search demand (Rezi, Cronen Squall, Axion, color settings). Fix already live: SEO CAPTIONS v2 on all scheduled posts since 24.11. Test window runs to 01.12.; first v2 posts go live today 12:00.
- Topic fix: new slots only use CSI terms with volume (type 73 mw4 164K, mw4 aim assist 278K rising) – no niche guns.
- Process fix: the pre-post re-check found that the Nov 23 DMZ tuning nerfed the Patriot XMR in DMZ, while today's caption said "after 3 Season 1 buffs" for MP + DMZ. Caption corrected. New rule: the re-check must read the newest patch notes for EVERY mode a post mentions (MP, Warzone, DMZ), not only the mode of the buff.

## 2026-11-25 – slot test 10:00 vs 12:00 (user approved: "Ja")
- Metricool best-time (TikTok, Berlin time, week 23.–29.11.): weekday peaks 10:00 > 18:00 ≈ 12:00 (e.g. Wed 1432 / 1386 / 1359, Thu 1471 / 1378 / 1299); weekend about 40 % lower, peaks 10:00 + 12:00.
- Own data 01.–24.11.: no clear difference 12:00 vs 18:00 – topic decides (search share 85–97 % on top posts).
- TEST 26.11.–02.12.: midday slot at 10:00 instead of 12:00, evening slot stays 18:00. Everything else unchanged (one variable).
- Measure on 03.12.: views + For You share of the 10:00 posts at day 1 and day 3 vs the 12:00 posts of 17.–25.11. at the same age (docs/reach-snapshots.csv). Keep 10:00 only if clearly better (For You share / early views), otherwise back to 12:00.

## 2026-11-26 – early warning run
- ALARM (continues from 25.11.): (1) search share of the last 3 posts below 50 % (pistol ranking 11 % at ~14 h, Patriot XMR 31 % at age 1, Rezi 12 37 % at age 2) while early-Nov build posts sit at 86–97 %; (2) color settings 316 views at age 4 = 35 % of the age-4 median (892). Rezi 12 is the worst post at age 2 (264 vs median 415).
- Likely cause: young posts (search share builds over days: Rezi 34 % -> 37 % in 1 day), niche topics with low search demand (color settings, Rezi, pistols), and the SEO v2 captions only live since 25.11. (too early to judge). No status problem: no post near 0 views (pistol 214 after ~14 h).
- First signal for SEO v2: Patriot XMR (first v2 caption) 390 views at age 1 = best age-1 value of the last week (median 298). n = 1, keep watching.
- Fix in this run: Sat 28.11. filled only with high-demand topics: KG-7 Vulcan build (#1 sniper in MP + Warzone, CSI 'Mw4 snipers' 213K) at 10:00 and 'movement settings mw4' (CSI 421K / 724K, never posted) at 18:00. Scheduled posts 26.–27.11. re-checked: captions v2, wallpaper renders, no patch notes after Nov 23 -> no change needed. Slot test 10:00 untouched.
- Rule added (process): render.py slide names use the image basename (subfolder paths like mw4/w_X.png crashed the render); single-gun build posts must use build_render.py (per-build mode badges) – the verifier caught WARZONE badges on MP/DMZ slides from render.py.

## 2026-11-27 – autopilot run: posts parked, no new posts scheduled
- Found: the 4 CoD posts for 27.–28.11. (Type 73 build, MW4 aim assist, KG-7 Vulcan build, movement settings) were changed on 26.11. ~11:00 to Metricool DRAFTS dated 28./29.12. (same "parking" pattern as the paused GTA posts). No note in the repo or reach log explains it → treated as a deliberate pause; the autopilot did NOT re-schedule or fill slots and asked the user.
- Numbers (no alarm): SEO v2 posts Oden 561 (age 1, 68 % search), Mosin 495 (age 1), Patriot 460 (age 2) vs pre-v2 Rezi 320 / LMG 443 at similar age. No post near 0 views, statuses all PUBLISHED.
- Rule: any run that parks/pauses posts must log the reason in docs/reach-log.md so the next run knows whether to fill the slots.
