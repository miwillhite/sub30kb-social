# sub30kb-social

Auto-posting pipeline for SubThirtyKB (@sub30kb).

## How it works

1. **posts.json**: the content queue. One entry per post (date, type, on-image fields, caption).
   Types match the approved Instagram designs: `card` (Mon), `carousel` (Wed), `sub10` (Fri), `cue` / `mantra` (weekend).
2. **render.py**: renders each post to PNGs in `out/<id>/` using `templates/` (Barlow fonts from `node_modules/@fontsource`).
3. **Commit + push**: images get public URLs at
   `https://raw.githubusercontent.com/miwillhite/sub30kb-social/main/out/<id>/NN.png`.
4. **Buffer**: a weekly Claude scheduled task creates *drafts* in the sub30kb Buffer account
   (Instagram + Threads; TikTok as photo posts) for the coming week. Matt approves them in the Buffer app.

## Weekly routine (what the scheduled task does)

- If `posts.json` has fewer than 2 weeks of posts left, draft the next week from the subthirtykb.com archive
  following the cadence, and flag any new Sub-10 that needs a test run.
- `npm ci && python3 render.py --from <next Mon> --to <next Sun>`
- commit + push `out/`
- create one Buffer draft per post per channel, `customScheduled` at 6:30 AM PT on the post date, `saveToDraft: true`.

## Local use

```
npm ci
pip install jinja2 playwright && playwright install chromium
python3 render.py --from 2026-10-26 --to 2026-11-01
```
