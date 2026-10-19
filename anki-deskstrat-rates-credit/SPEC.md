# Card-writing spec (VP-level Desk Strat interview, Rates & Credit, London)

Audience: candidate preparing for VP desk-strat interviews at a London investment bank (sales/trading-desk strat, structuring strat, pricing-quant blend). No behavioural questions.

## Quality bar
- Not surface level: every card must test mechanism, derivation, edge case, market convention, or a trade-off a senior interviewer would probe. No definitions a graduate would know unless they are a stepping stone to a deeper follow-up.
- No fluff, no pop-science, no motivational text. State-of-the-art, post-2022 conventions (SONIA/SOFR RFR, LIBOR cessation, RPI-CPIH alignment in 2030, ISDA 2014 credit definitions, FRTB/SA-CCR/SIMM, etc.) where relevant.
- Be factually careful. If a number is a rule of thumb, say "approx." Do NOT invent precise figures, dates or citations you are not sure of. If unsure, omit the detail rather than guess.
- Answers should be structured: short headline answer first, then the reasoning/derivation, then "Interviewer follow-up:" line with the likely probe and the key point of its answer where useful.
- Mix of: conceptual-why, derivations (MathJax), numerical/mental-math with worked numbers, scenario ("what happens to X if Y"), and trade-off cards.
- Each card must be self-contained and unambiguous; one testable idea per card (a derivation may have several steps in the answer).

## Output format
Write a single valid JSON file (UTF-8) at the path given in your task: a JSON array of objects:
{"type": "basic" | "cloze", "front": "...", "back": "...", "tags": ["lowercase_tag", ...]}

- For "basic": `front` = question (HTML), `back` = answer (HTML).
- For "cloze": `front` = text using Anki cloze syntax {{c1::...}} (HTML), `back` = optional extra explanation (HTML, may be "").
- HTML only: use <b>, <i>, <br>, <ul><li>, <ol><li>, <code>, <table>. No markdown.
- Maths: Anki MathJax, inline \( ... \), display \[ ... \]. Remember to escape backslashes for JSON (write \\( and \\frac).
- Use cloze for facts/conventions/formulas with 1-3 deletions; use basic for everything requiring reasoning. Roughly 20% cloze.
- 2-6 tags each, e.g. "swaps", "multicurve", "derivation", "mental_math", "scenario", "coding", "convention".
- Validate your JSON by running: python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(len(d))" <path>  and fix errors.
- Write the file with the Write tool or a Python script. Aim for the card count given in your task.

## Depth expansion (v2) — additional rules
Target: make the reader a top-decile rates/credit quant-strat. Every new card must be at least as hard as a final-round VP question at a top-tier bank.
Three formats are required in every new file, in roughly equal measure:
1. **Follow-up chains**: 3-5 linked basic cards simulating an interviewer drilling down on one topic (base question -> "why" -> edge case/failure mode -> derivation or numbers). Front of each card starts with `<b>[Chain: SHORT_NAME n/N]</b>` and recaps the context in one line so the card stands alone. Tag with `chain_short_name`.
2. **Full derivations**: step-by-step, every step justified (measure change, Ito, replication argument, approximation used and its error order). End with "Where it breaks:" line. Tag `derivation`.
3. **Worked case studies**: a realistic multi-step problem with concrete numbers (notional, rates, spreads, vols), solved step by step with intermediate results, final answer, and a sanity check. Tag `case_study`. Do the arithmetic carefully (use python to verify every number).
Also keep ~15% cloze for must-know formulas/conventions.
Use python3 to verify every numerical result before writing it.

## v3 expansion — additional rules
v3 adds a foundations layer, a C++ course, a desk-practice layer, reinforcement of thin subdecks and gap topics. All earlier rules still apply (HTML, MathJax, JSON schema, answer structure, factual care, python-verified numbers).

**Difficulty tag (mandatory, exactly one per card):** `lvl_foundation` (graduate-quant baseline the rest of the deck assumes), `lvl_vp_core` (what a VP candidate must answer cleanly), `lvl_stretch` (top-decile / final-round curveball). Tags may go to 7 including this one.

**No duplicates:** `verify/existing_fronts_v2.txt` lists every existing card front by file. Read the part relevant to your topic first and do not repeat a card already there; go deeper or adjacent instead.

**Foundations cards (`lvl_foundation` mostly):** teach, do not just test. Answer structure: one-line answer → intuition → precise statement/formula → small worked example with numbers → "Used in the deck for:" line naming where it reappears (e.g. "annuity measure in swaption pricing"). Build chains that climb from basic to the level the VP cards assume. Still no fluff: no "finance is important" sentences.

**C++ course cards:** the learner is a quant who knows Python but little C++. Each card teaches one idea with a short, complete, compilable snippet in `<pre><code>` (HTML-escape `<`, `>` and `&` inside code as `&lt;` `&gt;` `&amp;`). Compile every snippet that has a `main` (or wrap it in one) with `g++ -std=c++20 -Wall -Wextra -O2` in a scratch dir and fix errors before writing. Answer structure: what it is → code → what the code prints/does → "Interview trap:" line (the classic mistake or follow-up). Mix basic cards, cloze for syntax/rules, "what does this print / what is wrong with this code" cards, and implement-it cards.

**Desk-practice cards:** make the candidate sound like they have sat on a London rates/credit desk. Concrete workflows, numbers, timings, systems-agnostic where vendor specifics are uncertain (say "the booking system", not invented screen names). Bloomberg functions only if certain (e.g. YAS, SWPM, CDSW, OVML, VCUB, ALLQ, BVAL). Scenario style: "It is 16:15, the P&amp;L explain shows X unexplained — walk through how you find it". Answers give the exact steps, the checks, the numbers, and the trader/risk/control-function angle. No behavioural/HR questions; every card must have a technical answer.

**Writing method:** build the cards in a python script (a list of dicts) and dump with `json.dump(cards, f, ensure_ascii=False, indent=1)`; for >30 cards write in 2-3 scripts appending to the same list via an intermediate JSON. Validate at the end and print the count and the tag counts for lvl_*.

## Layered explanations (mandatory for all new cards)
Backs are layered, each layer short and only when it has content: **Answer** (one sentence) → **Intuition** (plain-words why) → **Precise** (formula/statement/numbered steps) → **Worked example** (numbers to final result) → **Trap / Where it breaks** → **Interviewer follow-up** / **Used in the deck for**. C++ cards: Answer → Code → Output → Why → Interview trap. Desk scenarios: Answer → Steps → Numbers → Control angle → Follow-up. Diagrams are appended last in `<div class="fig">`. `tools/check_layering.py` enforces that restructuring never changes fronts, tags, code, figures, maths or numbers.
