# Flywheel website

The static site for **Flywheel**, an open-source toolchain that helps formal libraries of mathematics and theoretical computer science in Lean agree with each other: semantic search, canonicity checking, harmonization, proof quality, and faithfulness checking. There's no build step and no dependencies beyond Google Fonts.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, the problem, how it works, tools, roadmap, people |
| `about.html` | About: the problem, approach, principles, open questions |
| `tools.html` | Tools: each tool in brief, with the canonicity-check figure |
| `roadmap.html` | Roadmap: phases and gates, workstreams, measures of success |
| `partners.html` | Partners: partner roles, how libraries connect |
| `governance.html` | Governance: steering committee and maintainers (with photos), reference process, contributions, contact |
| `contributing.html` | Get Involved: ways to take part, community |
| `resources.html` | News & Resources: news, papers, teaching, related work |

Content is condensed from the Flywheel whitepaper, roadmap, and slide deck (Nov 2026). Pages are kept short, in line with CSLib (about 100 to 400 words per page).

The pages link `style.css?v=<hash>` and `app.js?v=<hash>`, where the hash is a fingerprint of the file's contents. Whenever either file changes, the hash in every page must be updated too, or browsers and the GitHub Pages cache keep serving the old file. The header and footer are the same on every page. If you change a nav link or a footer link, change it in all eight files.

Placeholders are marked `[TBD]`, and links not yet live are `href="#"`. List them with `grep -n "TBD\|href=\"#\"" *.html`.

## Other files

- `style.css`: all styles. Colors and spacing are tokens in `:root`. Type is the Source family (Source Serif 4, Source Sans 3, Source Code Pro). The last block, "editorial revision", overrides the earlier card styles.
- `app.js`: the Copy button and small progressive enhancements. The pages work without it.
- `static/`: `logo.svg` and `favicon.svg`; the figures `fig-problem.svg`, `fig-overview.svg` (home) and `fig-canonicity.svg` (Tools), which are inlined into the pages; `people/` (headshots, 480 px squares, from each person's homepage or institutional profile); and `backup/` (earlier figures, kept for reference).
- `figures/src/`: the figure sources. `figstyle.py` is copied from `paper-figures/`; `web.py` adds `write_svg`, which emits web SVG in the site's fonts. Rebuild a figure with `python3 figures/src/<name>/figure.py`, then paste the new SVG into the page that uses it.
- Partners are not yet confirmed. Partner listings are kept as HTML comments in `index.html`, `partners.html`, `roadmap.html`, and `governance.html`; remove the comment wrapper to restore them.

## Preview

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy

Push to GitHub and enable Pages (Settings → Pages → deploy from `main`, root).
