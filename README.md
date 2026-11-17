# Project page template

A static, single-page project site for a research paper: no build step and no dependencies beyond Google Fonts.

- `index.html`: the page, with one placeholder example of each component (hero, TL;DR, mode cards, flow diagram, callout, figure split, tiles, figure walkthrough, results table, findings, ablation ladder, staged chart with tooltips, BibTeX).
- `style.css`: all styles; colors and spacing are tokens in `:root` (`--accent`, `--c1`–`--c3` for chart series).
- `app.js`: sticky nav and scroll-spy, reveal-on-scroll, the figure walkthrough, the staged chart, tooltips, and Copy-BibTeX. The page reads fine without it.
- `static/`: favicon and figures (`placeholder.svg` stands in for real figures).

## Preview

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Customizing

- Sections: each `<section id="…">` needs a matching link in both `.nav .links` and `.rail`.
- Walkthrough: each step's `data-region="left top width height"` (percent of the image) sets where the spotlight goes.
- Chart: `.mark` groups with `data-stage="n"` appear at step n; a `.hit` circle right after a mark gives it a tooltip (`data-name`, `data-val`, `data-sub`, `data-color`).
- Analytics: paste your own tag at the top of `<head>`.

## Deploy

Push to GitHub and enable Pages (Settings → Pages → deploy from `main`, root).
