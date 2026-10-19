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
