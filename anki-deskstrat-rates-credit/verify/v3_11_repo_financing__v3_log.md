# Verification log: cards/11_repo_financing__v3.json

Cards checked: 25 (21 basic, 4 cloze). Cards changed: 11. Card count and types unchanged.

| Card index | Issue | Fix | Source or method |
|---|---|---|---|
| 4 | Sponsor-as-counterparty stated without naming the model | Headline now says "sponsored-principal model" | Model convention (principal vs agency) |
| 7 | Gross SFT figure given as £10.0bn; card 8 uses £19.6bn | Changed to £19.6bn (£10.0bn + £9.6bn) | Internal consistency |
| 9 | Window dressing argued on a point-in-time basis; UK minimum uses averaged ratio (daily averaging for on-BS and SFT, month-end for other off-BS) | Answer now says the mechanism holds for point-in-time measures and adds a UK caveat | https://prarulebook.co.uk/guidance/supervisory-statements/ss45-15-the-uk-leverage-ratio-framework/3-averaged-leverage-ratio-calculation/05-08-2024?p=1 ; arithmetic recomputed (2.0/0.0325 = 61.54; 69.6 - 61.54 = 8.06) |
| 11 | Unescaped `<` in `\(c<f\)` (would be parsed as an HTML tag) | Escaped to `&lt;` | HTML validity check |
| 12 | Tie-back claimed £1.25m is 0.52% scaled to the book; it is not (0.52% x 150 = 0.78, x 163.04 = 0.85) | Reworded: £1.25m is the cost difference on the £150m book; shown as 153.06 x 4.02% = 6.15 vs 163.04 x 4.54% = 7.40 | Recomputed (python arithmetic) |
| 14 | Haircut sensitivity wrong: at 5% the repo capacity (475) is below 483.75, so the haircut binds, not equity | Recomputed: equity 25, cost 21.50m, effective rate 4.30%; rate flat for haircut below 3.25% | Recomputed |
| 18 | RONIA described as brokered gilt repo with an unsourced 2022 status claim | Front: "from sterling repo trades". Back: RONIA (Repurchase Overnight Index Average) is secured, not administered by the BoE (which administers SONIA); check current status | https://www.marketswiki.com/wiki/RONIA (weak source); BoE administers SONIA per search results |
| 19 | Balance-sheet channel stated without noting UK averaging | Added "point-in-time" qualifier and UK averaging caveat | As card 9 |
| 21 | SEC source line cited Rule 17ad-22(e)(18) without the sub-paragraph | Now cites order of 25 Feb 2025 and Rule 17ad-22(e)(18)(iv). Dates unchanged: cash 31 Dec 2026, repo 30 Jun 2027 | https://arnoldporter.com/en/perspectives/advisories/2025/03/us-treasury-clearing-sec-extends-compliance-dates ; https://www.theglobaltreasurer.com/2025/02/26/sec-grants-one-year-extension-on-treasury-clearing-rule-compliance/ |
| 24 | Cloze said RONIA built from brokered gilt repo; unsourced 2022 status claim | Cloze now "sterling repo"; back says RONIA not administered by BoE; check status | As card 18 |

Verified, no change needed:
- Card 8 and 9 numbers: gross 2/69.6 = 2.87%, netted 2/50.4 = 3.97% (recomputed).
- Card 1 numbers: 200/0.98 = 204.08; x0.97 = 197.96; x0.98 = 194.00; exposure 6.00 (recomputed).
- Cards 2, 16: gilts 6.153m vs corporates 7.402m, difference 1.25m (recomputed).
- Card 5, 17: netting reductions 76.9% and 96.6% (recomputed).
- Card 10: 96.75 x 4% + 3.25 x 10% = 4.195 (recomputed).
- Card 11, 15: fail vs borrow costs (recomputed).
- Card 13: netted exposure 0 (recomputed).
- Cards 8, 9, 10 (3.25% UK leverage minimum): confirmed against the PRA Rulebook, https://prarulebook.co.uk/guidance/supervisory-statements/ss45-15-the-uk-leverage-ratio-framework/ . Card 21 SEC dates confirmed as in the table above.
- Tags: exactly one lvl_* per card; max 6 tags per card. HTML: no other unescaped `<` or `&`.

Unverified or still doubtful:
- Card 0 and 3: tri-party intraday mechanics and "industry reform since 2010" are described generically; not checked against a primary source.
- Card 6: port timelines and segregation mechanics are generic ("depends on the CCP's rules"); not checked against a specific CCP rulebook.
- Card 11: fail-charge convention is generic. The US Treasury (TMPG) and UK/EU (CSDR) regimes differ and were not checked.
- Card 18, 24: RONIA's current administration and status could not be confirmed by search. Only a MarketsWiki page was found. Check the administrator's site before citing its status.
- Card 19: the claim that Swiss banks report on a quarter-end basis (used in card 9) comes from a secondary summary (finadium), not a primary source.
- Card 4: sponsored-principal vs agency model conventions at the specific UK CCP were not verified.
