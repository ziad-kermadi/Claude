# Verification log: cards/15_found_deriv.json

Cards checked: 50 (basic 40, cloze 10). Cards changed: 19. Card count and types unchanged (50 cards). All numbers recomputed with python3 (`recomputed`). Each card has exactly one lvl_* tag. JSON validated.

| file | card index | issue | fix | source URL or "recomputed" |
|---|---|---|---|---|
| 15_found_deriv.json | 1 | Net cash flow written as 5.00-100.00+95.12=0.123 (arithmetic gives 0.12) | Use Ke^{-rT}=95.1229, net 0.1229 | recomputed |
| 15_found_deriv.json | 5 | Said that p>1 (u=1.02) makes "borrowing to buy the stock" a riskless profit. Wrong direction: when e^{rh}>u the stock returns less than cash, so the arbitrage is short stock and lend. Raw < inside MathJax | Corrected arbitrage direction; escaped < as &lt; | recomputed |
| 15_found_deriv.json | 10 | Said r=0 but used r=5% gamma (0.0188) and theta (-3.75). At r=0, gamma = phi(0.1)/(S sigma) = 0.01985 and theta = -3.970/yr, -0.01088/day | Replaced with r=0 values; breakeven 1.047 unchanged | recomputed |
| 15_found_deriv.json | 11 | Expected hedged P&L used r=5% gamma: 94 x 0.0225 = 2.12. Correct at r=0: 99.2 x 0.0225 = 2.23 | Corrected gamma-based numbers to 99.2 and 2.23 | recomputed |
| 15_found_deriv.json | 15 | Raw < in MathJax (sigma_K<0) | &lt; | n/a (escape) |
| 15_found_deriv.json | 19 | Interviewer answer said "the put's extra theta" is the interest on strike; put theta is less negative (benefit), wording misleading | Reworded: call pays strike financing cost -rKe^{-rT}N(d2), put gets +rKe^{-rT}N(-d2) | recomputed (call -6.414, put -1.658) |
| 15_found_deriv.json | 21 | ATM forward-start value 100(2N(0.11916)-1)=9.485, shown as 9.48. The 0.4 S sigma sqrt(tau) rule gives 9.53, not 9.51; 1/sqrt(2pi) rule gives 9.51 | Price 9.49; rule restated as 1/sqrt(2pi) | recomputed |
| 15_found_deriv.json | 23 | Digital value 0.532325 -> GBP 532,325 (said 532,323). 0.01-wide spread = 0.5322 (said 0.5323). Skewed digital 0.551075 -> GBP 551,075 (said 551,087); correction GBP 18,750 (said 18,800) | Corrected three figures | recomputed |
| 15_found_deriv.json | 26 | Dividend-yield extension said "replace S with Se^{-qT} in F" (inconsistent) | Now F = S e^{(r-q)T} | recomputed (standard form) |
| 15_found_deriv.json | 27 | Back said e^{rh} >= u is arbitraged by buying stock with borrowed money. That loses money; the arbitrage is to short stock and lend. Raw < in MathJax | Corrected direction; &lt; | recomputed |
| 15_found_deriv.json | 34 | Said -ln P / tau is a concave function of the Gaussian bond price. -ln is convex; the convexity comes from Jensen applied to E[exp(-int r)] | Reworded | recomputed |
| 15_found_deriv.json | 42 | Term-scaling claim: 3m vega is "0.5 of 1y" only at the forward. Exact at S=K=100, r=5% is 19.64/37.52 = 0.52 | Stated as approximate at forward, exact 0.52 | recomputed |
| 15_found_deriv.json | 43 | Said vanna vanishes at the ATM-forward point. It vanishes at d2=0, i.e. K = F e^{-sigma^2 T/2} = 103.05, not at K=F | Corrected location | recomputed |
| 15_found_deriv.json | 47 | Said short-gamma hedging flows "pin" the price near expiry. Pinning is the long-gamma case; short gamma accelerates | Corrected both cases | n/a (conceptual) |
| 15_found_deriv.json | 48 | Raw < in MathJax (RR<0) | &lt; | n/a (escape) |
| 15_found_deriv.json | 49 | Said straddle delta is zero when strike equals forward. Zero at d1=0, i.e. K = S e^{(r+sigma^2/2)T} = 107.25 | Corrected strike and interviewer answer | recomputed |

Verified correct without change (recomputed): PCP values (C-P 4.877; forward-form 2.897; dividend-yield drop 1.980); binomial 1-step (p=0.7564, price 7.19, delta 0.5, B=-42.81); 2-step call 10.87 and nodes 15.11; American put root 2.48, European 1.35, premium 1.13; BS call 10.45, put 5.57, delta 0.637/-0.363, gamma 0.0188, vega 37.5, theta call -6.41 and put -1.66; PDE identity 0.52 = rV; Black-76 10.45; Hull-White theta(1)=0.86%; lognormal mean 105.13, median 103.05, 5%/95% 74.16/143.19; Vasicek 1y 3.21%, 5y 3.60%, 30y 3.86%, asymptote 3.92%; caplet bracket 0.001435 and GBP 34,803; digital 0.5323; 100/101 spread 0.5230; forward-start vol 23.8%; dividend forward 102.01 (6m: 102.05), put 8.59; real-world P 0.655, risk-neutral 0.560; American call lower bound 24.88; dividend threshold 2.47; delta at S=110 0.796; implied vol Newton 22.66%; vanna -0.281; straddle delta 0.274, gamma 0.0375, vega 75.0, theta -8.07; risk reversal -3, butterfly 0.5; 188 shares per 10,000 options.

## Sources checked (web)
- Hull-White theta formula: https://www.metricgate.com/docs/hull-white-model/ (secondary; consistent with my derivation). Original Hull and White (1990) not reached.
- Forward vs futures sign with positive rate correlation: Ritchken chapter notes https://faculty.weatherhead.case.edu/ritchken/textbook/chapter2ps.pdf (secondary); Cox, Ingersoll, Ross (1981) J. Financial Economics 9(4) 321-346, DOI 10.1016/0304-405X(81)90002-7, https://ideas.repec.org/a/eee/jfinec/v9y1981i4p321-346.html (abstract only).

## Unverified / still doubtful
- Card 17 (Hull-White theta) and card 36 (futures sign): confirmed only from secondary sources; the derivation in the cards is checked algebraically.
- Card 40 (dividend exercise threshold D > K(1-e^{-r(T-t)})) is a standard first-screen rule of thumb, not an exact condition; the card already says so.
- Card 45 (skew explanations) is qualitative; no figures, not web-checked.
- Card 23 skew -0.0005 per unit strike is a hypothetical input, not a market quote.
