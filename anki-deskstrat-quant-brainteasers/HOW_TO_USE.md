# How to study this deck

Import `DeskStrat_Quant_Brainteasers_VP_London.apkg` into Anki. It lands under `DeskStrat VP London::Quant Interview Core`, next to the rates and credit deck.

## Why it is built this way (the evidence)
| Design choice | Mechanism | Evidence |
|---|---|---|
| Every card asks you to **name the structure first** | Experts sort problems by deep structure; novices sort by surface features. Transfer depends on noticing that structure. | Chi, Feltovich & Glaser (1981), *Cognitive Science* 5 |
| **Twin cards**: the same structure in a different costume | Analogical transfer is rare from one example but improves a lot when you *compare* two cases that share a schema | Gick & Holyoak (1983), *Cognitive Psychology* 15; Gentner, Loewenstein & Thompson (2003), *J. Educ. Psych.* 95 |
| **Perturbation cards** ("what breaks if…") | Contrasting cases show *which* assumption carries the result, which is the real target of follow-up questions | Schwartz & Bransford (1998), *Cognition & Instruction* 16 |
| **Interleaved review** across subdecks | Interleaving trains you to *choose* the method, not just run it. Blocked practice feels better but tests worse. | Rohrer & Taylor (2007), *Instructional Science* 35; Kornell & Bjork (2008), *Psych. Science* 19 |
| Retrieval rather than re-reading, with spacing | Testing and spacing effects | Roediger & Karpicke (2006); Cepeda et al. (2006), *Psych. Bulletin* 132 |
| "Say it out loud" prompt | Self-explanation: you learn more when you explain each step to yourself | Chi et al. (1989), *Cognitive Science* 13 |

## The review protocol (this is the part that matters)
1. **Study the whole parent deck, not one subdeck at a time.** Interleaving is the point. Use the subdecks only for the first pass through new material.
2. On every problem card, before you flip it, **say three things out loud**:
   - the structure;
   - the feature of the wording that triggered it;
   - the first line of the solution.

   Grade yourself on whether you named the structure correctly, not just on whether you got the number right.
3. Give yourself 60 to 90 seconds of real attempt. If you get nothing, flip it and grade **Again**. A failed attempt before seeing the answer still helps you learn (the "pretesting" effect).
4. After flipping, read the **Transfer** line and invent one more problem with the same structure in your head. That takes about 10 seconds and builds the schema.
5. **Weekly filtered decks by structure.** In Anki, use Tools → Create Filtered Deck with a search like `tag:s_symmetry` or `tag:s_optional_stopping`. Reviewing all cards that share one structure but look different is the comparison step from Gentner et al.
6. **Weekly recognition-only sprint.** Search `tag:fmt_recognise`, set a 20-second timer per card, and only name the structure. This is what fast recognition in an interview needs.
7. **Mock-interview mode** (last two weeks). Search `tag:fmt_chain` or `tag:fmt_perturb` and answer out loud as if speaking to the interviewer: answer first, then reasoning, then a sanity check.

## v2: rebuild, don't recall
The deck is built so you can **regenerate** answers from a blank page. Recognising an answer when you see it is not the goal.

| Card type | Tag | What you do | Why (evidence) |
|---|---|---|---|
| Rebuild | `fmt_rebuild` | Derive a canonical result from a minimal seed on paper. Only the *move* is worth memorising. | Generation effect (Slamecka & Graf 1978) |
| Connect | `fmt_connect` | Derive result B from result A, so one remembered result regenerates many | Elaboration builds an integrated schema (Dunlosky et al. 2013) |
| Debug | `fmt_debug` | Find the single wrong line in a confident but wrong solution | Erroneous examples improve transfer (Große & Renkl 2007; Adams et al. 2014) |
| Estimate first | `fmt_estimate` | Bounds and limiting cases in 30 seconds, before any algebra | This is the interviewer's sanity check, practised ahead of time |
| Generate | `fmt_generate` | Invent a problem that *forces* a given structure | Producing examples shows you understand the structure's boundaries |
| Code | `fmt_code` | Write the 10 lines that verify the answer | Interviews often end with "now simulate it" |
| Hint ladders | `hints` on problem cards | Open hints only when stuck: 1 is a question, 2 names the move, 3 sets up the first line | Faded scaffolding (Renkl & Atkinson 2003) |

**Grading rule (strict):**
- Solved without opening a hint: **Good**.
- Needed hint 1 or 2: **Hard**.
- Needed hint 3, or saw the back: **Again**.

**Rebuild sessions.** Twice a week, search `tag:fmt_rebuild` and do 5 cards on blank paper with the screen hidden. Only flip once you have a full derivation or are truly stuck. A result you can rebuild is one you no longer need to remember.

**Error log.** Search `tag:err_*` to see your recurring error types. The **Smell** line on each debug card is a detector to run on your own live answers.

## Suggested settings
- New cards per day: 25 (the 1,220 cards take about 7 weeks to introduce; use 35 a day if your interview is under 6 weeks away). Maximum reviews: 300.
- Use FSRS with desired retention 0.90. Raise it to 0.95 in the final two weeks.
- Leave "Bury related new cards" on so chain cards are spread across days.

## Tag cheat-sheet
- `s_*`: structures (for example `s_reflection` or `s_linearity_expectation`).
- `fmt_recognise`, `fmt_solve`, `fmt_perturb`, `fmt_twin`, `fmt_toolkit`, `fmt_chain`, `fmt_rebuild`, `fmt_connect`, `fmt_debug`, `fmt_estimate`, `fmt_generate`, `fmt_code`: card formats.
- `err_*`: error classes on debug cards.
- Topic tags such as `dice`, `options`, `random_walk`, `mental_math`.

To rebuild after editing cards: `pip install genanki && python3 build.py`.
