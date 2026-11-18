# news-image-20261117 — Round 3 handoff (bright-badger-10)

## Entry
- Title: "The Day in World News - Tuesday 17 November 2026 (48 stories, 6 continents)"
- entry.png: 1024x1024, 201,462 bytes,
  sha256 `2000d8f2f40202114bef7b5e881303f503bec8ef1b2ce0db1a883283aeea4bb0`
- Design (fresh v3, not a variation of r2): navy masthead + gold kicker,
  red ticker, 18 uniform illustrated cards in a 3x6 grid (no lead hierarchy),
  numbered world map with leader-line pins 1-18 + 30-item list 19-48 below.
  All 18 illustrations drawn in code with PIL flat-vector shapes.
- Build dir: `~/workspace/makefun/news-image-20261117-r3/`
  (build.py, entry.png, main.py, README.md, LICENSE, .makefun/owner.json)
- r2 files were NOT read (per task); facts only from result files + fresh
  searches this session.

## Determinism
- build.py run 2x: identical sha256
  `2000d8f2f40202114bef7b5e881303f503bec8ef1b2ce0db1a883283aeea4bb0`
- main.py run 2x (stdlib only, no network): identical sha256, matches entry.png.

## 48 stories + sources
Cards 1-18 (title + deck on image):
1. Kerch Bridge road span dropped into the sea - Reuters/AP 17 Nov
2. Iran drones at US radar in Bahrain; US hits Qeshm - Reuters/AP 17 Nov
3. Trump first Quad summit, Manila; Shenzhen Thu talks - Reuters/AP 17 Nov
4. Nvidia sales double to $115.8bn, revenue +103% - company results/Reuters
5. JPMorgan bug cuts off Zelle users; not a cyberattack - AP 17 Nov
6. Dow -849 (-1.6%), S&P 500 -1% - market wires 17 Nov
7. Ebola 11,000+ cases in DR Congo, 5,400 dead - WHO
8. Mongolia president says he will resign; parliament must accept - Reuters
9. Japan scrambles jets, 2 planes near Okinoshima - Japan MoD/Reuters
10. Five EU states plan Rwanda asylum hub; no deal signed - Reuters
11. Vulcan rocket fails; 40 Amazon satellites lost (launch 15 Nov, ULA update 17 Nov)
12. Voyager 1 nears one light-day; NASA public lights event Tue night - NASA
13. US, Mexico, Bolivia lose measles-free status; US 5,400+ cases - PAHO
14. French public-sector strike; 146,000 march (ministry) / 500,000 (CGT) - Le Monde/AFP
15. Bangladesh police tear-gas garment workers; want Tk 30,000 - AFP/Reuters
16. Turkey seizes Sozcu TV; channel off air, trustee named - Reuters
17. COP31 Antalya final days split on fossil fuels/finance - Reuters
18. Serbia Student List 140/250 takes seats; Vucic party to opposition - Reuters

Briefs 19-48 (one line each on image):
19. Gaza: UN warns winter crisis; 1.4m hungry - UN News 17 Nov (reworded:
    the "truce at risk of collapse" warning is dated 18 Nov, not 17 Nov)
20. Russian An-12 crash in Siberia kills all 19 - Reuters
21. Cyclone Akvan grows; Odisha evacuates - IMD/IANS 17 Nov
22. UK sanctions 8 firms over West Bank sites - UK govt/Reuters
23. Eisenkot elected Knesset speaker, 66-52 - Knesset/Times of Israel
24. Pope Leo XIV back from South America tour - Vatican News
25. WHO: superbugs could kill 39m by 2050 - WHO/AFP (16-17 Nov)
26. US data centres emit like Denmark: study - Harvard/Nature Sustainability,
    Reuters 16-17 Nov (403 centres, 25.7m tonnes CO2)
27. Ecuador fishermen sue US over boat strike - Reuters 16-17 Nov
28. Mexico: journalist found dead in Acapulco - Reuters/AP
29. PNG defends closing Taiwan office - Reuters 17 Nov (Marape to Xi, Shenzhen)
30. Football: Canada beat Guatemala 4-1 - match reports
31. Poland: Tusk survives vote, 242-200 - Reuters
32. Nepal: loss-and-damage first - UNFCCC/COP31
33. Moldova shuts airspace as drone nears - Reuters
34. Haiti: Aristide party fields no candidates - Reuters 15-16 Nov
35. Pentagon fails audit for ninth year - DoD
36. NSA secret network down; no sign of hack - CNN/Nextgov 17 Nov
37. Home Depot sales beat forecasts - company results
38. Brazil Senate delays fiscal vote - Reuters
39. Singapore seeks trusted AI-chip access - AFP/Straits Times 17 Nov
40. World Court hears Myanmar case - ICJ
41. Bezos helped cast Pattinson as Bond - Reuters/USA Today 17 Nov
42. Cyclone Xavier hits Cat 5, winds 220 km/h - JTWC
43. German ZEW jumps to 35.6, beats forecasts - ZEW
44. Depardieu drops appeal - AFP
45. Seoul scrambles jets as Russian planes near (KADIZ, no airspace violation)
    - Yonhap/AFP 17 Nov
46. Japan economy contracts - Cabinet Office/Reuters
47. UK PM tests EU reset before summit - Reuters
48. US-Thailand sign trade statement; $2.6bn farm buys - White House/AgWeb
    17 Nov (reworded: joint statement, final deal still to be signed)

Verification: items 19, 21, 25, 26, 27, 29, 34, 36, 39, 41, 45, 48 were
re-verified by fresh web search in this session. The rest follow the task
brief and the prior rounds' verification records (result.md / result-r2.md).
Deliberately NOT used (unverified per brief): Quad patrol flights/export
curbs, COP31 $20m heat plan, Gaza 93,000 tents, Serbia "ending Vucic rule".

## QA (full-size + 300px + zone crops, all read)
Defects found and fixed:
1. Map pin 1 (Kerch) completely hidden behind pin 16 (Istanbul) - added
   leader-line label offsets for all crowded pins (1, 4, 5, 6, 7, 10, 11, 12,
   13, 16, 17, 18) plus a red dot at each true position.
2. Map pins 7/10 merged into one "710" blob - separated with offsets.
3. US pins 4/12/13 piled into one blob; 18/16 overlapping - separated.
4. "12 tracked from NASA JPL, California" note struck through by the footer
   rule - removed the line; note moved into the map header.
5. Antarctica strip cut off at the map box edge - Antarctica polygon dropped
   (cropped world map); map rescaled to fill the box better.
6. North America shape too blobby - added Hudson Bay notch to the polygon.
7. Rocket illustration read as a small diamond - redrew as a bigger rocket
   with window and flame.
8. False alarm, not a defect: light dashes above the masthead title were the
   tops of the serif letters in "November".
Final pass: no typos, no clipped/overlapping text, all 18 pins distinct and
readable, briefs 19-48 complete and legible, footer clean. No em-dash or
en-dash anywhere (file is pure ASCII).

## Push
- Base: remote HEAD 579efb3779849bc050a545ce1c3abaae8d312974 (r2 commit)
- New commit: (filled after push)
- Push: fast-forward only, no force-push. Verified via git ls-remote.
- NOT submitted to make.fun (coordinator's task).
