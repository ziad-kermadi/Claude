# Verify log: 17_cpp_m3.json and 17_cpp_m4.json

Method: every `<pre><code>` program in the 80 cards (HTML-unescaped) was compiled with `g++ -std=c++20 -Wall -Wextra -O2` (g++ 13.3.0, libstdc++ 13) and run. Diagnostics were compared with the card text, and the file names used in the cards were reused so that diagnostic locations match. Sanitizer claims were checked with `-fsanitize=address` and `-fsanitize=leak` builds. Fold-expression naming was checked against the standard text via search (cppreference mirror and N4659 [expr.prim.fold]). Numbers were recomputed with python3. HTML escaping was checked: no raw `<`, `>` or `&` inside `<pre><code>`, and MathJax delimiters are `\( \)`. Each card has exactly one `lvl_*` tag. Card count (40 + 40) and types are unchanged.

## Changes

| File | Card index | Issue | Fix | Source |
|---|---|---|---|---|
| 17_cpp_m3.json | 2 | LSan block was shown without its frame lines but presented as the full report | Added "(stack frames omitted)" | compiled and run, -O0 -fsanitize=leak |
| 17_cpp_m3.json | 25 | Said ASan reports the crash as a SEGV inside printf. ASan actually reports a SEGV in std::string::size() called from main. The exit status -11 is shown by shells as 139 | Corrected the ASan location and the status wording. Also checked with ASAN_OPTIONS=detect_stack_use_after_return=1; result is the same | compiled and run, -fsanitize=address |
| 17_cpp_m3.json | 34 | Cache explanation for the column walk was wrong: it said neighbouring elements are not reused before eviction. The column working set (2048 lines, 128 KiB) exceeds L1, and the 16 KiB stride touches 2048 pages, which exceeds the L1 dTLB. The prefetcher does not follow the stride across pages. The timings (row 4.3 to 5.4 ms, column 20.6 to 22.6 ms over 5 runs) are within the ranges already stated | Rewrote the mechanism paragraph; numbers kept | compiled and run, 5 repeats |
| 17_cpp_m4.json | 11 | Said the unnamed `= 0` parameter makes the two templates distinct. The distinction comes from the two different enable_if conditions | Reworded | compiled and run; reasoning from the standard's template-parameter equivalence rules |
| 17_cpp_m4.json | 17 | `(xs + ... + 0)` called a binary left fold. The form `(pack op ... op init)` is a binary RIGHT fold | Renamed to binary right fold and gave the expansion | WebSearch: N4659 [expr.prim.fold] (https://www.ece.uvic.ca/~frodo/cppdraft/n4659/html/expr.prim.fold) and cppreference mirror (https://cppreference.net/cpp/language/fold.html) |
| 17_cpp_m4.json | 18 | Said the error is "correct as written for non-empty packs" (confusing) | Reworded: template accepted; error only at instantiation with an empty pack | compiled and run (diagnostic matched) |
| 17_cpp_m4.json | 20 | Said the empty-pack case never arises. The second call passes an empty tail, which is valid (comma fold of empty pack is void()) | Corrected the sentence | compiled and run, output "done" |
| 17_cpp_m4.json | 23 | Card showed a static assertion error with a message, but the code shown had no message. The error line was also tied to a file name that was not compiled | Added the message to the static_assert in the text and gave the key error line without a file location | compiled: `static_assert(std::is_base_of_v<Instrument<Bond>, Bond>, "CRTP argument must name this class")` fails as stated |

## Checked and correct (no change)

- All program outputs in both files match the compiled runs, including m3 c04, c05, c06, c08, c09, c13, c14, c15, c16, c17, c18, c19, c20, c22, c23, c26, c27, c29 (fixed version), c30, c31, c32, c35, c36, c37; m4 c00 to c39 except c23 above.
- Diagnostics checked against the card text: m3 c05, c22, c25, c28; m4 c01, c10, c13, c18, c26, c27, c39 (linker message; the two-file build with an explicit instantiation prints 9).
- Sanitizer claims: m3 c02 (LSan at -O0 reports 4000 bytes; at -O2 no report, and the -O2 assembly contains no operator new[] call), c19 (double-free), c28 (alloc-dealloc-mismatch), c29 (bad-free, "16 bytes inside of 24-byte region"), c35 (clean under ASan).
- Recomputed numbers: discount factors 1/1.05^t, Pricer scenarios 2.89692 and 24.5988, bond PV 95.2381, memory figures (120 MB vs 60 MB; 320 MB and 80 MB), 2048 x 8 bytes = 16 KiB and 32 MiB.
- sizeof claims: unique_ptr 8 and 16 with function-pointer deleter; shared_ptr 16; Bad 12 / Good 8; Empty 1, WithBase 8, WithMember 16; std::function 32 on libstdc++.
- std::is_pointer_v<int* const> is true; std::exp and std::pow are accepted as constexpr by g++ 13 in C++20 mode with no pedantic warning (card wording "as an extension" kept; the standard does not guarantee it).
- HTML: no unescaped `<`, `>`, `&` inside code. MathJax uses `\( \)`.

## Unverified / remaining doubts

- m3 c10: "an uncontended atomic is typically on the order of ten to twenty cycles (approx.)". Not measured here; left as an approximate statement, which the spec allows.
- m3 c34: timings are machine-specific. The card says they come from this sandbox and gives a range; they were reproduced here.
- m3 c02 and c27: whether -O2 removes the leak is compiler-specific (verified for g++ 13 only). The card states this for g++ 13.
- Sanitizer and linker output in cards is trimmed (frames, process ids, file paths). Process ids differ on every run and were not reproduced exactly.
- m4 c27: libstdc++ accepts constexpr std::exp and std::pow in C++20 mode. This is a library extension, not guaranteed by the standard. The card says so.
