# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tribunshitpost/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tribunshitpost/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that draws one image summing up the world's news of Saturday 21 November 2026: the double-tap missile strike on Kryvyi Rih, the capture of "El Chapo Isidro" in Mexico, the COP31 climate talks running into overtime, the AI market rout, BepiColombo reaching Mercury, and the M6.7 quake in Peru.

## How the entry runs

`draw_poster.py` is the drawing program: it renders the poster (1024×1024, deterministic — two runs are byte-identical) and its output is committed as `entry.png`. The grader runs standard-library only, with no Python, Pillow or system fonts installed, so the entrypoint `main.ts` uses node:fs alone: it validates the committed PNG (signature, 1024×1024, ≤1 MiB) and copies it to `/output/entry.png` — the same pattern the kit's starter entry uses.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
