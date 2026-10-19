# DeskStrat VP London — Rates & Credit Anki deck (v3)

Import `DeskStrat_Rates_Credit_VP_London.apkg` into Anki (File → Import). Re-importing updates existing cards (stable GUIDs).

- **1791 notes**, 302 cloze, **330 with a diagram** (PNG, white background, bundled in the package).
- Difficulty tags on every card: `lvl_foundation` 355, `lvl_vp_core` 1099, `lvl_stretch` 337. Study in levels with tag searches.
- Subdecks: Rates ×5, Credit ×3, XVA & Funding, Structured Products, Markets/Regulation, **0 Foundations ×4** (probability, fixed income, derivatives, statistics), **Quant & Coding** (numerical methods + a 7-module **C++ course**, every snippet compiled with g++ -std=c++20), **Desk Practice ×9** (P&L explain, marking/IPV, booking/clearing, market making, credit desk, client flows & event days, risk limits, strat tooling, market episodes).
- Answers are layered: Answer → Intuition → Precise → Worked example → Trap → Follow-up (foundations, C++ and desk-practice cards).
- Every new file was fact-checked and recomputed in Python; logs in `verify/`. Remaining unconfirmed points are listed in the logs (e.g. Bobl tick size omitted).
- Sources: `cards/*.json`; diagrams `media/`, mappings `diagram_maps/`. Rebuild: `pip install genanki && python3 tools/apply_diagrams.py && python3 build.py`. Rules: `SPEC.md`.
