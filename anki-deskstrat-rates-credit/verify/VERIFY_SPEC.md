# Fact-check pass rules

You are verifying Anki cards for a VP desk-strat interview deck. Accuracy is the only goal.

1. Load WebSearch/WebFetch via ToolSearch ("select:WebSearch,WebFetch") and use them. Prefer primary sources: ISDA, BoE, DMO, ONS, LCH, CME/ICE/Eurex contract specs, BCBS/PRA/SEC texts, original papers (Hagan 2002, Pedersen, Burgard-Kjaer, Andersen-Broadie, etc.) or reputable textbooks/notes.
2. For every card in your files, check:
   - Dates, thresholds, regulatory numbers, contract specs, conventions, historical events -> verify by web search when not certain.
   - Formulas and derivations -> check signs, factors, measure, limits. Re-derive or check numerically with python3.
   - Worked numbers -> recompute with python3. Fix the arithmetic and every dependent number.
   - Units (bp of yield vs price points, per 100 face vs notional, annual vs daily vol).
   - Internal consistency between cards.
3. Fix errors in place, editing the JSON via a python script (load, modify, dump with ensure_ascii=False, indent=1). Keep the same number of cards, same types, valid JSON, Anki MathJax \( \) with JSON-escaped backslashes. Keep the existing answer structure.
4. If a fact cannot be verified, keep it and add " (approx.; unverified)" where it appears. Do not invent sources.
5. Write a log to verify/<prefix>_log.md: a table of every card changed (index, file, what was wrong, the fix, source URL or "recomputed"), then a list of unverified items.
6. Validate the JSON at the end. Only touch your assigned files and log.
7. Final report: number checked, number fixed, the most important corrections, remaining unverified items. Keep it short.
