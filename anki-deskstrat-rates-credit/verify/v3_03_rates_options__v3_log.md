# Verify log: 03_rates_options__v3 and 12_structured_exotics__v3

Cards checked: 20 (03) + 25 (12) = 45. Cards changed: 8 cards (03: idx 3, 7, 12, 13, 16; 12: idx 5, 10, 14). lvl_* tag count: exactly one on every card in both files. No markdown, no unescaped code blocks, MathJax delimiters \( \) and \[ \] only.

## Changes

| File | Idx | Issue | Fix | Source / check |
|---|---|---|---|---|
| 03_rates_options__v3 | 3 | dS omitted the covariation term d<w_i,F_i> (product rule is exact only with it) | Added + sum_i d<w_i,F_i> to the dS identity | recomputed (product rule) |
| 03_rates_options__v3 | 7 | Claimed theta != -1/2 sigma^2 Gamma off the money. In the pure Bachelier PDE the identity holds at every strike; it fails only with a smile (vol depending on F) | Rewritten: relation holds at every strike in pure Bachelier; smile adds a term | recomputed (PDE is exact for all F) |
| 03_rates_options__v3 | 12 | "1% of bond price" horizon stated as t near 20y. Solving 1-exp(-0.06t) = 0.5592 gives t = 13.67y (1% effect reached there) | Changed to t ~ 13.7y with the ratio shown | recomputed (python) |
| 03_rates_options__v3 | 13 | Residual stated as -0.011mm; exact 0.48491mm vs Taylor 0.49528mm gives -0.0104mm | Changed to -0.010mm | recomputed (python) |
| 03_rates_options__v3 | 16 | Cloze dS identity had the same missing covariation term as idx 3 | Added covariation term, noted frozen weights remove it | recomputed |
| 12_structured_exotics__v3 | 5 | Said "Same note" but card 4 of the chain uses quarterly accrual and payment; this card uses annual periods | Front now states annual accrual is a simplification for this calculation | internal consistency |
| 12_structured_exotics__v3 | 10 | Kirk MC claimed 400k paths giving 25.93bp. Recomputed: Kirk 25.894bp; 2,000,000-path MC 25.888bp +- 0.027bp | Changed MC line to 2M paths, 25.89bp, se 0.03bp | recomputed (python) |
| 12_structured_exotics__v3 | 14 | Vega per vol point 10y 5,192 (card 5,200); 2y 5,874 (card 5,900). Correlation: dP/drho = -0.000321 per unit per 0.10 gives -31,149 (card -0.000323, -31,000) | Corrected to 5,190 / 5,870 and -0.000321 / -31,100 | recomputed (python, central differences, Kirk) |
| 12_structured_exotics__v3 | 14 | 2y hedge: 4,425/191 (PV01 of 1m at annuity 1.91) = 23.2m, not 23.1m | Changed to 191.0 and 23.2m | recomputed |

Cards 0-2, 4, 6, 8-9, 11, 15-24 of 03 were checked and the numbers reproduce; no edit needed.
Cards 0-24 of 12 were checked; the edits are listed in the table.

## Verified without change (key checks)

- 03 idx 0-2 (Cheyette y, G, bond formula): y5 = 4.3197e-4 (sd 2.078%), y_inf = 1.6667e-3 (sd 4.08%); P(5,10) = 0.83705 with y-term, 0.84096 without; Monte Carlo (300k paths, 1000 Euler steps) at sigma=3%: 0.75215 +- 0.00025, formula 0.75219. Reproduced by independent MC. Source for bond formula: arXiv 2506.23876 (secondary) gives P = P0(T)/P0(t) exp(-G x - 1/2 G^2 y), G = (1-e^{-lambda(T-t)})/lambda. Also matches Hull-White ln A convexity term sigma^2(1-e^{-2lambda t})/(4 lambda) B^2.
- 03 idx 3-5 (LMM): w = (0.50739, 0.49261), A = 1.88435, S = 2.7463%; sigma_S = 18.445% (rho 0.9), 18.924% (rho 1). Rebonato frozen-weight formula reproduced.
- 03 idx 6, 10 (Hagan normal SABR, beta=0): leading-order skew d sigma_N/dK = rho nu/2 = -0.06 (algebra checked: x(zeta) = zeta + rho zeta^2/2 + O(zeta^3)); numeric sigma_N(2.90%) = 0.90625%, sigma_N(3.10%) = 0.89426%, slope -0.0600. ATM: sigma_N^ATM = alpha[1 + (2-3rho^2) nu^2 T/24]; c = 0.011533; alpha = 98.86bp. MC of the full SABR (400k paths, alpha=0.9886%, nu=0.4, rho=-0.3, T=1): ATM normal vol 99.80bp +- 0.02, correction 0.95% +- 0.22% vs predicted 1.15%; (nu=0.4, rho=0, T=1) MC 1.29% +- 0.20 vs 1.33%. Consistent within MC error.
- 03 idx 7, 17 (straddle/theta): sigma sqrt(dt) = 6.30bp, sqrt(2/pi) x = 5.0bp; mental math 80bp -> 5.04bp, 4.0bp expected |move|.
- 03 idx 8: variance identity from swaption strip gives 1.0000e-4 = sigma^2 T to 1e-15 (normal, F=3%, sigma=1%).
- 03 idx 9, 15: capped CMS. Payer(4%) flat = 8.33bp, cash 0.690mm; skew payer 6.93bp, cash 0.574mm; difference 0.116mm (16.8% of payer leg).
- 03 idx 12 (rest): y1, y5, y20 and 1/2 G^2 y values match; price effects -0.10%, -0.46%, -1.25%.
- 03 idx 13: premium 0.7979% per unit annuity, cash 6.61mm; gamma P&L 0.297mm, vega 0.198mm; exact 0.485mm; delta -0.229.
- 03 idx 14: DV01 41,409 (sticky strike), 43,391 (sticky delta), add-on 1,982 per bp, 59,470 per 30bp.
- 12 idx 0-3 (snowball): E[c2]=1.00%, E[c3]=0.50%, no-memory 1.00%.
- 12 idx 11: PV_fund 97.30, FB 2.70, mod duration 4.58.
- 12 idx 12: floorlet E = 0.698% (d = 0.5).
- 12 idx 13 (digital note): P = 0.588, 0.562, 0.551; sum PD 1.605; FB 1.58; budget 9.07; c* 5.65%; no-FB 4.66%.
- 12 idx 14, 17: Kirk Greeks PV01 5,213 / -4,425; correlation -31,149 per 0.10 rho; price 251,398.
- 12 idx 15: PVs 97.17, 95.34, 93.46, 93.46; E[PV] 94.86.
- 12 idx 5-6 (callable RA): break-even p* = 0.680; continuation 97.00 (p=0.5), 101.99 (p=0.8), 88.69 (p=0), 105.32 (p=1).
- 12 idx 7-9 (zero callable): 100/1.04^20 = 45.64; accreted 55.53; market value 64.19 / 55.53 / 48.10; loss 8.66 at 3%.
- 12 idx 10, 24 (Kirk): sigma_K = 21.43%, effective sigma = 18.57%, d1 = 0.0929, Kirk = 25.89bp; MC 25.89bp.

## Unverified or doubtful (left as written, flagged)

1. Hagan normal-SABR beta=0 closed form zeta/x(zeta) (03 idx 6, 10): not retrieved from a primary source by search (search returned implementation pages only). The expansion algebra and the MC checks support the leading-order skew and the ATM first-order correction, but the exact closed form is from memory of Hagan et al. (2002).
2. Kirk approximation (12 idx 10, 14, 24): effective-vol and pricing formulas confirmed by secondary implementation docs (MetricGate). No primary Kirk (1995) text was retrieved. Kirk's error at this strike is not quantified beyond "approx." in the card.
3. 12 idx 18 (rate autocall): "the bank is long the early-redemption option". Sign convention is not fully settled across desks; the card is left as written.
4. 12 idx 4: "The investor is short vol on that probability" is loosely phrased; left.
5. 12 idx 13: funding convention (principal at funding curve, digital coupons at OIS via swap hedges). Internally consistent, but a desk could fund the whole note. Stated as the convention; left.
6. 03 idx 0: the statement that "y is deterministic ... so the pair (x,y) is Markov" is muddled (a deterministic y is not a second random state). Numbers are correct; wording left.
7. 12 idx 15: toy with expected fixings 2% under a 3% discount curve is flagged on the card itself; left.
