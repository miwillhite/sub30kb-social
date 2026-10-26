# sub30kb-social

Auto-posting pipeline for SubThirtyKB (@sub30kb).

## How it works

1. **posts.json**: the content queue. One entry per post (date, type, on-image fields, caption).
   Types match the approved Instagram designs: `card` (Mon), `carousel` (Wed), `sub10` (Fri), `cue` / `mantra` (weekend).
2. **render.py**: renders each post to PNGs in `out/<id>/` using `templates/` (Bebas Neue + Barlow from `node_modules/@fontsource`).
   Templates follow **design system v2** (Oct 25 2026): bone ground on every feed post, Bebas Neue display, the workout as a
   "ledger" (number first in a fixed left column, in ink, never orange), one orange element per post (the hero number),
   time tag as an inverted pill top-right, badge lockup + `@sub30kb` in the footer.
   Content rules: per-side work is written `5/5`; carries and holds are in seconds (`30s` renders as `30 S`), never meters.
   Cards take an optional `hero`/`hero_label` (minutes); otherwise the hero is the round count from `instruction_lead`.
3. **Commit + push**: images get public URLs at
   `https://raw.githubusercontent.com/miwillhite/sub30kb-social/main/out/<id>/NN.png`.
4. **Buffer**: a Claude scheduled task (Thursdays 7:35 AM PT) creates *drafts* in the sub30kb Buffer account
   (Instagram + Threads; TikTok as photo posts) for the coming week. Matt approves them in the Buffer app.

## Weekly routine (what the scheduled task does)

- If `posts.json` has fewer than 2 weeks of posts left, draft the next week from the subthirtykb.com archive
  following the cadence, and flag any new Sub-10 that needs a test run.
- `npm ci && python3 render.py --from <next Mon> --to <next Sun>`
- commit + push `out/`
- create one Buffer draft per post per channel, `customScheduled` at 6:30 AM PT on weekdays / 7:30 on weekends, `saveToDraft: true`.
  Threads gets only `#kettlebell` (Threads tags one topic per post).

## Local use

```
npm ci
pip install jinja2 playwright && playwright install chromium
python3 render.py --from 2026-10-26 --to 2026-11-01
```
