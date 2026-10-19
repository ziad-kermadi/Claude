# Verify log: cards/17_cpp_m6.json

Toolchain: g++ 13.3.0 (Ubuntu), `-std=c++20 -Wall -Wextra -O2 -pthread`, host x86_64 (`-march=native` = sapphirerapids). perf not installed on the host.

Cards checked: 40 (all). Code blocks extracted, HTML-unescaped, compiled and run: every block containing `main` (about 45 programs, including -O0, -O1 and TSan/ASan variants) plus the fragments and asm claims.

| file | card index | issue | fix | source or basis |
|---|---|---|---|---|
| 17_cpp_m6 | 17_cpp_m6 | 1 (back) | Bare `&` in "int&" (HTML validity) | Escaped to `int&amp;` | HTML rule |
| 17_cpp_m6 | 2 (back) | Sample -O0 numbers presented as "real output"; the value is nondeterministic | Relabelled as nondeterministic; replaced with six observed runs (994931 to 1322614). -O2 result 2000000 and `addl $1000000, counter(%rip)` confirmed; TSan race confirmed | compiled, run, asm |
| 17_cpp_m6 | 5 (back) | "four synchronisations" miscounts the local version (it has no lock in the loop) | Reworded | recomputed (sum 0..999999 x 4 = 1999998000000) |
| 17_cpp_m6 | 14 (back) | seq_cst load mapping stated as "usual", not checked | Checked: seq_cst load is plain `movl`; store `xchgl` confirmed | compiled, asm |
| 17_cpp_m6 | 15 (back) | "GCC warns about its use in a header (-Winterference-size)" not reproduced: no warning with a header, a template, or -O2/-mtune/-march variants; web search did not confirm the default | Removed the warning claim; kept the tuning-dependence point | compiled; https://gcc.gnu.org/pipermail/libstdc++/2024-September/059490.html (inconclusive on defaults) |
| 17_cpp_m6 | 18 (back) | Headline called it only a data race; ASan shows stack-use-after-scope (dangling reference to a for-loop local). Output lines were garbled and presented as fixed | Headline rewritten (ASan + TSan); output relabelled nondeterministic with observed values | compiled, ASan, TSan, six runs |
| 17_cpp_m6 | 20 (back) | Corrected program not shown, only the one-line wait and "consumed 42" | Added complete corrected program; front compiles with no diagnostics | compiled, run three times, prints `consumed 42` |
| 17_cpp_m6 | 21, 22, 33 (back) | Distribution output is implementation-defined; labels lacked the library | Labelled libstdc++ / GCC 13; noted the identical-counts property in 22 holds on any implementation | compiled, run |
| 17_cpp_m6 | 24 (back) | "19,937-bit state" is imprecise | Changed to 624-word state, period 2^19937 - 1 | standard MT19937 property (not web-checked) |
| 17_cpp_m6 | 28 (back) | Scratch directory path leaked into the compiler report | Replaced with `vec_saxpy.cpp:` prefix; report text matches GCC 13.3 exactly | compiled with -fopt-info-vec-optimized |
| 17_cpp_m6 | 29 (back) | Explanation said GCC "judges profitable" and implied 256-bit reduction; the FP sum is kept in source order (no -ffast-math), and the vfmadd is in the scalar tail | Rewritten; counts re-checked (default: 0 ymm; native: 4 ymm, 1 vfmadd; -ffast-math: 4 ymm, 2 vfmadd) | compiled, asm |
| 17_cpp_m6 | 32 (back) | "main contains no divsd (no division at all)": sum_recip is still emitted, just not called | Reworded; volatile-sink variant verified (main contains a divsd) | asm |
| 17_cpp_m6 | 34 (back) | Claim row-major is faster had no timing | Added five-run timing (row 4 to 8 ms, col 24 to 37 ms; nondeterministic) | timed on this host |
| 17_cpp_m6 | 35 (front, back) | Atomic max is wrong for -0.0 (it satisfies x >= 0 but has the largest bit pattern); ran update_max(-0.0), update_max(5.0) and got -0 | Front comment and trap corrected; fix sentence added | compiled, run |

Recomputed (python3, no change needed): 5 (total), 17 (332833500), 22 (estimate 3.143536; SE 0.00164 single, 0.00082 four streams, ratio 2), 25 (2^50 draws at 1e9/s = 13.03 days), 26/27 (32 B records, 320 MB vs 80 MB, 16 ms vs 4 ms at 20 GB/s), 36 (S(8) 5.93, S(16) 9.14, S(64) 15.42, limit 20, Gustafson 7.65), 37 (N = 1,440,000; 72 s single core; 12 s on 8 threads at 75%), 6 (Amdahl with s = 1/101 on 4 threads: 3.885).

Confirmed as stated (no change): 0 (SIGABRT, 134, stdout empty when redirected), 1 (GCC 13.3 error text identical; fixed output 1), 4, 8 (hang), 9, 11 (2000000, is_always_lock_free = 1), 12, 13 (TSan race at -O1), 16 (nodiscard warning and order), 17, 19, 26, 30 (1000 / 0, checksum 999000), 31 (0 / 1 allocation, 11.5), 35 (1999.5 after fix), 38 (perf not run: not installed; labelled in card).

Unverified / still doubtful:
- 25: xoshiro256** jump() equals 2^128 steps: attributed to Blackman and Vigna; not re-checked against the primary source in this pass.
- 15: "some ARM designs use 128-byte lines" is marked approx. in the card; left as is.
- 38: perf commands and flags were not executed (perf not installed).
- 25 back contains "xoshiro256**"; the `**` is part of the generator name, not markdown.
