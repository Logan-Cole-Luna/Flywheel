# Flywheel website

The static site for **Flywheel**, an open initiative building AI-for-math tooling for Lean and the unified, formally verified library of computer science it produces. There's no build step and no dependencies beyond Google Fonts.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, four feature cards, the flywheel walkthrough, sponsors and partners |
| `about.html` | About: why now, what this enables, open by design |
| `contributing.html` | Get Involved: ways to contribute, Zulip, the Lake snippet |
| `roadmap.html` | Roadmap: two pillars (tooling, library), directions, phases |
| `governance.html` | Governance: steering committee, maintainers, contact |
| `partners.html` | Partners: partner projects, how they connect, supporting organizations |
| `resources.html` | News & Resources: news, docs, meetings, papers |

The header and footer are the same on every page. If you change a nav link or a footer link, change it in all seven files.

Placeholders are marked `[TBD]`, and links not yet live are `href="#"`. List them with `grep -n "TBD\|href=\"#\"" *.html`.

## Other files

- `style.css`: all styles. Colors and spacing are tokens in `:root` (`--accent`, `--c1`–`--c3`).
- `app.js`: reveal-on-scroll, the flywheel walkthrough (each step's `data-region="left top width height"`, in percent of the image, places the spotlight), and the Copy button. The pages work without it.
- `static/`: `favicon.svg`, `flywheel.svg` (the loop diagram), `placeholder.svg`. Put partner logos in `static/logos/`.

## Preview

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy

Push to GitHub and enable Pages (Settings → Pages → deploy from `main`, root).
