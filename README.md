# news-image-20261117 — Round 2

One image that sums up the world news of **Tuesday 17 November 2026**:
front page "THE WORLD IN ONE DAY", 42 stories from 6 continents.

## What is on the page

- Masthead: "THE WORLD IN ONE DAY", TUESDAY, 17 NOVEMBER 2026.
- 3 illustrated leads: Kerch Bridge down; US strikes Iran, Tehran says
  it hit a US radar site in Bahrain; Quad meets in Manila, Trump flies
  on to Shenzhen for Xi and Putin.
- A world map with 12 numbered pins, one per illustrated story.
- 9 illustrated story cards: Ebola in DR Congo, COP31 in Antalya,
  measles-free status lost, Nvidia's $115.8bn quarter, Gaza tents and
  aid, Mongolia's president quits, Serbia's student MPs sworn in,
  Bangladesh garment workers demand Tk 30,000, An-12 crash in Kemerovo.
- "ALSO ON TUESDAY 17 NOVEMBER": 30 more stories, one line each
  (13-42), from Japan scrambling jets to the Quad's 2027 patrol flights.
- Honesty footer: every story happened or was first reported on
  Tuesday 17 November 2026; disputed claims are attributed.

## Files

- `entry.png` — the entry, 1024x1024 PNG.
- `build.py` — draws `entry.png` from scratch with Pillow
  (flat-vector illustrations, all drawn in code; no copied images).
  Run it with `python3 build.py`. Deterministic: two runs write
  identical bytes.
- `main.py` — the program the grader runs (Python 3.13, standard
  library only): copies `entry.png` to `/output/entry.png`.
- `LICENSE` — MIT.

## Sources

Reuters, AP, AFP, BBC, Al Jazeera, UN News, WHO, IPC, ZEW,
MetService. Each story was checked against reporting dated
17 November 2026 before it was drawn.
