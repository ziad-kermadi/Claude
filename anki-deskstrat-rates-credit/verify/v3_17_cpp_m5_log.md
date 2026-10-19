# Verification log: 17_cpp_m5.json and 17_cpp_m7.json

Scope: 80 cards checked (40 per file). Index is the 0-based position in the JSON array.
Method: every snippet with main() was extracted (HTML-unescaped), compiled with
g++ 13.3 -std=c++20 -Wall -Wextra -O2, run, and compared with the stated output.
Sanitizer and assertion claims were run with -fsanitize=address and -D_GLIBCXX_ASSERTIONS.
Numbers were recomputed with python3. Escaping checked: no unescaped < > & inside any
<pre><code> block. Each card has exactly one lvl_* tag. No markdown in fronts or backs.

| File | Index | Issue | Fix | Source or method |
|---|---|---|---|---|
| 17_cpp_m5 | 5 | Buggy erase loop was described but its code was missing from the card | Added the buggy snippet to the back (before the stated output) | Compiled and run: prints `5 -1 7` as stated |
| 17_cpp_m5 | 9 | Stability program was missing; the output had no source. Trap said insertion sort applies "about 16 or fewer" | Added the full program. Reworded the trap: insertion sort for 16 or fewer elements; the check passes for 6 and 16 trades and fails for 17 and 40 | Program reproduces the stated output exactly; sizes tested by compile and run |
| 17_cpp_m5 | 19 | Front asks what the buggy legs return; the back never said | Added: at -O2 this build prints `110 110 110`, undefined behaviour (dead storage) | Compiled and run |
| 17_cpp_m7 | 3 | "Both estimates within about one standard error" is wrong for the printed values | Changed to "about 1.1 to 1.2 standard errors" | Recomputed from printed values: (10.4794-10.4506)/0.0234 = 1.23; (10.4692-10.4506)/0.0165 = 1.13 |
| 17_cpp_m7 | 4 | Where-it-breaks example "straddle centred on the forward" is not even in Z, so the claim is wrong | Replaced with payoffs even in Z (\|Z\|, Z^2), which give rho = 1 and double the variance; antithetic helps only if rho < 0 | Derivation: f(Z)=f(-Z) gives rho = 1; run output (ratio 1.993) agrees |
| 17_cpp_m7 | 7 | Back said CRR u, d match "the mean and variance" of the log-return; only the variance is matched by u, d | Changed to variance; drift carried by p | Derivation: E[log return] under p depends on p |
| 17_cpp_m7 | 13 | "C++ silently does nothing with []" is wrong | Changed to: no check, reading past the end is undefined behaviour | Language rule (C++ [] is UB out of range) |
| 17_cpp_m7 | 18 | Chain card says AD matches to about 1e-15; run gives 7.1e-15 for vega | Changed to "within about 1e-14" | Run output: 3.331e-16, 7.105e-15 |
| 17_cpp_m7 | 21 | Front says bs_call calls erfc; it is norm_cdf that calls erfc | Front now names norm_cdf<T> | Code read |
| 17_cpp_m7 | 23 | QuantLib header paths and the LazyObject name were not verified (search returned no header paths) | Removed header paths and LazyObject name; kept verified concepts (RelinkableHandle::linkTo, observers, engines); pointed to the API reference for the version used | Search: https://www.quantlib.org/quep/quep005 and https://pyquantlib.readthedocs.io/en/latest/handles.html |
| 17_cpp_m7 | 26 | "1bp price accuracy ... billions of paths" was vague | Now: absolute error 0.0001 on 10.45 (about 1e-5 relative) needs about 8e10 plain paths at sd 14.7 | Recomputed: (1.96 x 14.7217 / 1e-4)^2 = 8.32e10 |
| 17_cpp_m7 | 27 | Python test output had no script | Added test_bsmod.py; module built with g++ -std=c++20 -O2 -shared -fPIC against pybind11 3.1.0 and Python 3.13. Output reproduced exactly (3 numbers and the TypeError line) | Built and run on this machine |
| 17_cpp_m7 | 36 | Timing in output was a captured run that did not match a fresh run | Output updated to a fresh run: 0.343 s / 0.074 s, 4.7x; second run gave 4.0x | Run twice; checksum and max difference unchanged |

Checked and correct without change (compiled and run, or recomputed): all other cards
in both files, including the Black-Scholes, MC, CRR tree, implied-vol, curve bootstrap,
Greeks and AD values, the sanitizer reports (heap-use-after-free, stack-use-after-return,
stack-use-after-scope, double-free), the GCC 13 warning texts (-Wtype-limits,
-Woverloaded-virtual, -Wuse-after-free), the _GLIBCXX_ASSERTIONS message, the
compile error for seconds = 1.5s, and the Python sizes (float 24 B; 32.9 B per element
in a list of 1000 floats).

Unverified or doubtful (kept, with caution):
- 17_cpp_m7 idx 23: QuantLib class names are from a search summary only; header paths removed.
- 17_cpp_m7 idx 36: timings are machine-specific; the card says so.
- 17_cpp_m7 idx 17: h* about 1e-5 is a rough estimate and is marked "approximate" in the card.
- Card cross-references ("card 02", "card 10", "card 20", "card 34", "card 36") use 1-based deck order and are consistent with this file; they are fragile if the deck is reordered.
- 17_cpp_m5 idx 9 and 17_cpp_m7 idx 27: the two stdout lines that depend on the standard library version (libstdc++ 13) are labelled as this machine's output.
