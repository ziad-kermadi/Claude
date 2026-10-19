# active-memory handoff: DeskStrat VP London – Rates & Credit Anki deck

**Handoff #1** · 2026-10-19 · Lineage: #1 (2026-10-19): built v1 deck (450 notes), expanded to v2 (856 notes / 1,035 cards, 12 subdecks), fact-checked every card, pushed to GitHub.

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** Anki deck with subdecks to prepare for **desk strat interviews in Rates and Credit in London, VP level**. No behavioural questions.
- **Done looks like:** questions/answers well formatted and not surface level; user's words: "I need more questions, I need you to make me one of the best quants in the market."
- **Why it matters / context:** interview preparation.

## 2. About the user (as relevant to this work)
- Candidate for VP desk-strat roles (Rates & Credit), London. GitHub user `ziad-kermadi`.
- Uses Anki; works through Claude Code cloud sessions (files are not local — must be fetched from GitHub or the chat file card).

## 3. Style & communication
- **Language:** English.
- **Tone:** direct, technical, no fluff.
- **Reply length:** concise status updates; summaries list concrete corrections/numbers.
- **Formatting:** markdown headings/bullets/tables in chat. Cards: HTML (`<b>`, `<br>`, `<ul>`, `<table>`, `<pre><code>`), Anki MathJax `\( \)` / `\[ \]`, no markdown in cards.
- **Working style:** ask the user about any decision or choice (AskUserQuestion with options); Opus orchestrates, Haiku subagents do bulk writing/verification; commit and push after changes (a stop hook enforces it).
- **Avoid:** behavioural questions, surface-level cards, pop science, invented facts.

## 4. Hard rules (word for word)
1. "Always use Opus as orchestrator and Haiku as subagents." / mid-task: "If you need sub agents use Haiku"
2. "Never any fluff, common sense or pop science."
3. "Always rooted in research and state of the art science."
4. "Add any sections or sub topics you think fall in context even if I omit them."
5. "Ask me about any decision or choice."
6. "No focus on Behavioral questions please."
7. "Make the questions and aswered well formatted and not surface level"
8. "Always 100 pages pdf minimum if book requested" (not applicable so far)
9. Stop hook: uncommitted/untracked changes in the repo must be committed and pushed to the remote branch before ending a turn.

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Asked whether to spawn subagents with default model | Use Haiku for all subagents |
| 2 | Proposed a product scope list | "Add CLNs as well and credit curve construction. I WANT COMPLTE COVERAGE for everything" |
| 3 | Said files were pushed but did not say where to find them | Explain location: cloud session, not local — download from GitHub or the chat file card |
| 4 | Offered limited depth options | All depth types: chains, derivations, case studies, upgrade existing cards; plus all areas evenly and new subdecks |

## 6. Decisions
| Decision | Why |
|---|---|
| Strat flavour: blend of sales/trading-desk strat, structuring strat, quant-heavy | user's call |
| Format: `.apkg` built with genanki, MathJax, tags, nested subdecks | user's call (recommended option) |
| Card types: conceptual, derivations (MathJax), mental math, coding (Python/C++), scenario/trade-idea, plus anything relevant | user's call |
| v2 depth: follow-up chains, full derivations, worked case studies, upgrade weakest cards | user's call |
| v2 scope: all areas evenly + new subdecks XVA/funding, repo/financing, structured products/exotics | user's call |
| ~400 more cards in v2 | user's call |
| Fact-check old + new cards with web sources | user's call |
| Deck lives in repo `ziad-kermadi/claude`, folder `anki-deskstrat-rates-credit/` | user asked: "create a new folder in here and copy this deck into it" |

## 7. Changed / rejected
- v1 ~400 cards (actual 450 notes) → v2 856 notes / 1,035 cards (user asked for more depth)
- Card "Narrowed Reference Obligation" (concept not found; likely fabricated) → replaced by Standard Reference Obligation (SRO) card
- ❌ CSV/TSV delivery (user chose .apkg)
- ❌ Behavioural questions

## 8. Data & facts (exact)
| Subdeck (Anki name under `DeskStrat VP London::`) | Source files | Notes |
|---|---|---|
| Rates::1 Govies, Futures & Repo | 01_govies.json (47), 01_govies_deep.json (30) | 77 |
| Rates::2 Swaps & Curve Construction | 02_swaps_curves.json (55), 02_swaps_curves_deep.json (30) | 85 |
| Rates::3 Options & Vol | 03_rates_options.json (59), 03_rates_options_deep.json (30) | 89 |
| Rates::4 Inflation & Linkers | 04_inflation.json (42), 04_inflation_deep.json (30) | 72 |
| Rates::5 Repo, Financing & Balance Sheet | 11_repo_financing.json (45) | 45 |
| Credit::1 Bonds, CDS & Indices | 05_credit_cds.json (56), 05_credit_cds_deep.json (31) | 87 |
| Credit::2 Models, Curves & CLNs | 06_credit_models_cln.json (59), 06_credit_models_cln_deep.json (30) | 89 |
| Credit::3 Converts, Loans & CLOs | 07_converts_loans.json (36), 07_converts_loans_deep.json (30) | 66 |
| Quant & Coding::Numerical Methods | 08_coding_numerics.json (44), 08_coding_numerics_deep.json (30) | 74 |
| Markets::Scenarios, Microstructure & Regulation | 09_scenarios_markets_reg.json (52), 09_scenarios_markets_reg_deep.json (30) | 82 |
| XVA & Funding::XVA, Funding & Capital | 10_xva_funding.json (45) | 45 |
| Structured Products::Exotics & Structuring | 12_structured_exotics.json (45) | 45 |
| **Total** | 21 files | **856 notes / 1,035 cards** |

- Card JSON schema: `{"type": "basic"|"cloze", "front": HTML, "back": HTML, "tags": [2-6 lowercase]}`.
- Answer structure: headline → reasoning/derivation → "Interviewer follow-up:". Chains: front starts `<b>[Chain: NAME n/N]</b>`, tag `chain_*`; derivations end with "Where it breaks:", tag `derivation`; case studies tag `case_study`.
- Note models: "DeskStrat Basic" id 1607392319, "DeskStrat Cloze" id 1607392320; deck IDs = md5(name)[:8]; note GUID = genanki.guid_for(front).
- `build.py` maps `*_deep.json` to same subdeck (strips `_deep`), escapes stray `<`/`>` (inside MathJax → `\lt`/`\gt`), converts newlines to `<br>`.
- Key fact-check corrections (now in the cards): CTD = highest implied repo; TMPG fails charge = max(3% − reference rate, 0); recovery-lock buyer long recovery; index 65 vs intrinsic 58 → sell index protection, buy constituents (+7bp); no compensation for RPI-linked holders, RPI→CPIH from Feb 2030, judicial review dismissed 1 Sep 2022; UK RPI swap lag 2m; Long Gilt notional coupon 4%, deliverable 8y9m–13y; free-boundary SABR = Antonov–Konikov–Spector (2015), Doust 2012 = no-arbitrage SABR; FRTB PLA amber keeps IMA with surcharge, red loses IMA; MPoR floor 10bd, 20bd for >5,000 trades/illiquid, disputes double floor; MM14 60m for restructured bonds and loans, 30m others; governmental intervention only for Financial Reference Entities; BoE 2022 gilt purchases 28 Sep–14 Oct 2022, up to £5bn/day over 13 operations (£65bn), actual ≈ £19.3bn; UK Basel 3.1 1 Jan 2027, FRTB IMA 1 Jan 2028; UK/EU T+1 11 Oct 2027; US eSLR final rule 25 Nov 2025 effective 1 Apr 2026; SEC Treasury clearing 31 Dec 2026 cash / 30 Jun 2027 repo; ISDA USD 3M fallback spread 26.161bp; LCH USD SOFR discounting switch 16 Oct 2020; HW futures convexity ≈ 4.8bp (3y) / 11.8bp (5y).

## 9. People, terms & names
- **People:** none besides the user.
- **Terms & nicknames:** "desk strat" = desk strategist (front-office quant); "deep" files = v2 depth expansion cards.
- **Names in use:** repo `https://github.com/ziad-kermadi/claude` (branch `main`); local clone `/home/user/claude`; folder `anki-deskstrat-rates-credit/`; deck file `DeskStrat_Rates_Credit_VP_London.apkg`; root deck `DeskStrat VP London`; `SPEC.md` (writing rules incl. v2 depth rules); `verify/VERIFY_SPEC.md` and `verify/01_log.md`…`12_log.md`; `README.md`.

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| Anki deck `.apkg` | final v2 | `anki-deskstrat-rates-credit/DeskStrat_Rates_Credit_VP_London.apkg` on GitHub `main` | not opened in Anki itself; package validated (856 notes, 12 subdecks, 0 MathJax/cloze issues) |
| Card sources | final v2 | `anki-deskstrat-rates-credit/cards/*.json` | ~150 cards edited by fact-check |
| Fact-check logs | done | `anki-deskstrat-rates-credit/verify/*_log.md` | unverified items tagged "(approx.; unverified)" in card text |
| Builder | final | `anki-deskstrat-rates-credit/build.py` | `pip install genanki && python3 build.py` |
| Socratic plugin setup | not started | `~/.claude/socratic-config.json` absent | user never answered which types to enable |

## 11. Next steps
1. **Next action:** ask the user which next improvement they want (options offered: mock-interview mode with randomised chains; difficulty tags such as VP-must-know vs stretch; a further ~300-card round targeting weak areas after they start reviewing).
2. Optionally resolve remaining "(approx.; unverified)" items (Basel paragraph refs, Moody's WARF factors, iTraxx Crossover name count, Hull textbook Ho-Lee convexity form ½σ²T1T2 vs agent's σ²T1(T2−T1/2)).
3. After any change: rebuild with `build.py`, commit, push to `main`.

## 12. Open questions ⚠️
- Which next improvement? (mock-interview mode / difficulty tags / another ~300 cards / verify remaining unverified items / something else)
- Socratic plugin: which explanation types to enable? (names, "todos", or "ninguno")

## 13. Re-attach checklist
- Nothing to attach. Everything is in GitHub repo `ziad-kermadi/claude` (re-clone in the new session).

---
<sub>Audit: 13/13 sections · 9 rules · 4 corrections · 40+ data points · secrets removed: none found · generated by active-memory</sub>
