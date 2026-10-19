# Card-writing spec: Quant Brainteasers, Probability & Maths (VP Desk Strat, London)

Audience: a VP desk-strat candidate at a London investment bank. Interviewers are quants and traders who ask probability, brainteaser, mental-maths, stochastic-calculus, statistics and linear-algebra questions live, often with follow-ups that change one assumption. No behavioural content.

## The core idea: teach structures, not answers
Memorised answers do not transfer; recognised *structures* do. Every problem in an interview is a costume worn by a small number of reusable moves (symmetry, linearity of expectation, first-step conditioning, invariants, reflection, optional stopping, replication...). The deck trains three skills in order:
1. **Recognise**: from the surface of a problem, name the structure and say *which feature of the problem* triggered it.
2. **Execute**: carry out the key move cleanly and fast.
3. **Transfer and stress-test**: solve the same structure in a different costume, and predict what breaks when one assumption changes.

## Structure taxonomy (use these exact tags, prefix `s_`)
s_symmetry, s_linearity_expectation, s_indicators, s_first_step_conditioning, s_recursion, s_markov_chain, s_complement, s_bijection, s_stars_bars, s_inclusion_exclusion, s_bayes, s_invariant, s_parity, s_extremal, s_pigeonhole, s_backward_induction, s_optional_stopping, s_martingale, s_reflection, s_geometric_probability, s_order_statistics, s_memorylessness, s_generating_function, s_coupling, s_tail_sum, s_change_of_measure, s_replication, s_dimensional_analysis, s_taylor, s_convexity_jensen, s_sqrt_time_scaling, s_fermi, s_kelly_log_utility, s_eigen, s_lagrange, s_conditional_expectation_tower, s_clt_normal_approx, s_poisson_approx, s_variance_decomposition, s_game_theory_equilibrium, s_information_design, s_dynamic_programming
Each problem card carries 1-3 `s_` tags plus 1-3 topic tags (e.g. `dice`, `random_walk`, `options`, `mental_math`) plus one format tag (see below). The tags let the learner build filtered decks by structure.

## Card formats (use all; target mix given per file)
Format tag in brackets.
1. **Recognition** `[fmt_recognise]`: front = a problem statement + "<i>Before solving: which structure, and what in the statement triggers it?</i>". Back = structure name, the trigger feature, the one-line key move, then the answer in brief. ~25%.
2. **Solve** `[fmt_solve]`: full problem. Back layout, exactly these labelled lines:
   `<b>Answer:</b>` result first<br>
   `<b>Structure:</b>` name + trigger<br>
   `<b>Key move:</b>` the decisive step<br>
   `<b>Working:</b>` concise derivation with MathJax<br>
   `<b>Sanity check:</b>` limit case, bound, symmetry or quick simulation estimate<br>
   `<b>Transfer:</b>` 1-2 other problems (different surface) this move kills. ~35%.
3. **Perturbation / what breaks** `[fmt_perturb]`: front = a known problem with ONE assumption changed (biased coin, without replacement, absorbing barrier added, correlation introduced, player can stop early...). Back = which part of the original argument fails and why, the fix, and the new answer. ~15%.
4. **Twin** `[fmt_twin]`: a problem that is structurally identical to a classic but looks unrelated. Front does NOT name the classic. Back reveals the classic, the mapping between them, and the answer. ~10%.
5. **Toolkit / heuristic** `[fmt_toolkit]`: front = "When should you reach for X, and when does X fail?" or a cloze of the key identity. Back = triggers, the move, a canonical example, the failure mode. ~10%. Cloze allowed here only.
6. **Interviewer chain** `[fmt_chain]`: 3-4 linked cards drilling one problem (base, follow-up, generalisation, edge case). Front starts with `<b>[Chain: SHORT_NAME n/N]</b>` and recaps context in one line so each card stands alone. ~5% (counts within the totals above is fine).

## Quality bar
- VP final-round difficulty. Include the famous classics (they *will* be asked) but always with a perturbation or twin card so the learner owns the structure. At least half the cards should go beyond the standard "Heard on the Street"/"Green Book"/Zhou/Joshi set: harder variants, generalisations to n, follow-ups.
- No fluff, no pop-science, no motivational text, no history anecdotes.
- **Correctness is non-negotiable.** Verify EVERY numerical answer with python3 (exact fractions via `fractions.Fraction` or sympy where possible, and a Monte Carlo simulation of at least 10^5 trials for any probability/expectation whose derivation is non-trivial). If a simulation disagrees with your derivation, fix the derivation or drop the card. Never invent a result.
- Prefer exact answers (fractions, closed forms) plus a decimal approximation.
- One testable idea per card; self-contained; unambiguous problem statements (state independence, fairness, replacement, what "uniform" means).
- Answers are short and dense. The back should be readable in under 60 seconds.

## Output format
A single valid JSON file (UTF-8) at the path given: a JSON array of objects
`{"type": "basic" | "cloze", "front": "...", "back": "...", "tags": [...]}`
- HTML only: <b>, <i>, <br>, <ul><li>, <ol><li>, <code>, <pre>, <table>. No markdown.
- Maths: Anki MathJax, inline `\( ... \)`, display `\[ ... \]`. In JSON the backslash is escaped (`\\(`, `\\frac`). Simplest: build the list in a python script and `json.dump` it (ensure_ascii=False).
- Cloze uses `{{c1::...}}` in `front`; `back` is extra explanation (may be "").
- Validate: `python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(len(d))" <path>`.
