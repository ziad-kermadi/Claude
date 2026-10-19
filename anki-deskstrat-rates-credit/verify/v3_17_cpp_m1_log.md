# v3 verification log: 17_cpp_m1.json and 17_cpp_m2.json

Checked: 80 cards (40 + 40). Method: every snippet with `main` was extracted (HTML-unescaped), compiled with `g++ -std=c++20 -Wall -Wextra -O2` (g++ 13.3.0), and run. Stated outputs and diagnostics were compared with the actual output. Multi-file examples (m1 #1, #3) were built as separate translation units. Sanitizer claims (m1 #28, #33; m2 #6, #23) were checked with `-g -O1 -fsanitize=address`. Standard-rule claims (ODR, initialisation order, vector growth, UB status) were checked against C++20 rules. No web sources were fetched; the "source" column names the local check or the standard rule used.

Result: 72 snippets compiled and ran. Outputs matched except m1 #28 (garbage value, now described as such). Intentional-error snippets produced the stated diagnostics once the card was corrected.

## Cards changed

| file | card index | issue | fix | source |
|---|---|---|---|---|
| 17_cpp_m1.json | 3 | Said function templates are "implicitly inline". Only constexpr functions are implicitly inline. Templates may be defined in headers because the ODR permits identical definitions. | Reworded the sentence. | C++20 ODR and inline rules (standard, no web fetch) |
| 17_cpp_m1.json | 28 | Quoted one garbage value (1.139e-313) as the -O2 output. Freed-memory garbage differs on every run (three runs: 1.13494e-313, 1.13833e-313, 1.14205e-313). | Pre block shows one value, with a note that it changes between runs. | recomputed (run x3) |
| 17_cpp_m2.json | 0 | "snippet.cpp:9:17" private-access diagnostic was attached to code that never accesses `v` outside the class. | Card now says to add `std::cout << s.v;` to main; the stated diagnostic was reproduced. | recomputed (compiled) |
| 17_cpp_m2.json | 1 | Trap said a member "declared earlier but initialised later" would be read uninitialised. In this snippet an earlier-declared member is initialised first, so that is wrong. | Trap now describes a read of a member declared below the initialiser (the actual indeterminate-read case). | C++ declaration-order initialisation rule |
| 17_cpp_m2.json | 10 | "Three pushes cause two reallocations." With capacity going 0 to 1, 2, 4 there are three allocations. | Text now says three allocations (capacity 1, 2, 4). Counts 0/6 and 3/3 were already correct. | recomputed (run) |
| 17_cpp_m2.json | 11 | Code comment "deep copy: unlike Python's b = a[:]" is wrong: `a[:]` is a shallow list copy. | Comment changed to "independent copy: Python needs list(a) for this". Output unchanged. | Python list semantics (standard Python behaviour) |
| 17_cpp_m2.json | 13 | Diagnostic cited snippet.cpp:8:48 for a call that is commented out in the snippet. | Stated that uncommenting line 13 gives 13:15 with the same message (reproduced). | recomputed (compiled) |
| 17_cpp_m2.json | 19 | Hand-written `<=>` diagnostic (8:30) had no code shown. | Added the hand-written snippet; diagnostic is now 10:28 (reproduced). | recomputed (compiled) |
| 17_cpp_m2.json | 26 | Abstract-class diagnostic (7:12) had no code shown. | Added the snippet; diagnostic is now 9:12 (reproduced). | recomputed (compiled) |
| 17_cpp_m2.json | 27 | override and final diagnostics had no code shown and wrong line numbers. | Added both snippets; diagnostics are now 9:12, 4:20 (warning) and 12:8 (reproduced). | recomputed (compiled) |
| 17_cpp_m2.json | 29 | Said a pure virtual called from a constructor "is a runtime error". Per the standard this is undefined behaviour. | Reworded as UB, with the compile-time g++ warning quoted (reproduced). | C++ rule on pure virtual calls during construction (standard, no web fetch) |
| 17_cpp_m2.json | 35 | unique_ptr diagnostics (9:16, 3:8) had no code shown. | Added the snippet; diagnostics are now 6:16 and 2:8 (reproduced). | recomputed (compiled) |

## Checked and correct (no change)

- m1 #0, #1, #2 (linker errors, `pv` output 95, undefined reference text), #4-#9, #11, #12, #14-#18, #21-#25, #27, #30-#39: outputs and diagnostics reproduced; explanations checked.
- m1 #5, #7: `always_true(INT_MAX)` prints true at -O0, -O1 and -O2. With -fwrapv it prints true then false. The -O0 asm is `movl $1, %eax`, so the card's claim holds.
- m1 #3: duplicate-definition error and fixed output `1000 1000000` reproduced.
- m2 #2-#5, #7-#9, #12, #14-#18, #20-#25, #28, #30-#34, #36-#39: outputs reproduced. m2 #6: ASan double-free message reproduced (same address). m2 #23: fixed version has no leak report. m2 #38: terminate message is for `std::logic_error`, as stated.

## Unverified / notes

- Sanitizer reports quoted in the cards (m1 #28 heap-use-after-free, m1 #33 SEGV, m2 #6 double-free) are sample excerpts. Their PIDs and addresses vary per run. The first lines and the reported source lines match a local run.
- m1 #36 quotes output `0` for an uninitialised `int`. This is one run; the value is indeterminate.
- Several cards use the filename `snippet.cpp` and others `main.cpp` in diagnostics. Both are labels, not errors.
- No web sources were fetched for this pass.
