#!/usr/bin/env python3
"""Verify every numerical claim in staging/gap_A.json (gap batch A).

Card index = position in gap_A.json. Exact values use fractions/integers and
brute-force enumeration; Monte Carlo checks use >= 1e5 trials with printed SE.
Run: python3 staging/verify_gap_A.py
"""
import itertools
import math
import random
from collections import deque
from fractions import Fraction as F
from math import comb, factorial, sqrt

RESULTS = []


def check(idx, label, claimed, computed, tol=None):
    if tol is None:
        ok = claimed == computed
    else:
        ok = abs(float(claimed) - float(computed)) <= tol
    RESULTS.append(ok)
    print(f"card {idx:2d} [{label}] claimed={claimed} computed={computed} {'PASS' if ok else 'FAIL'}")


def lis_len(seq):
    tails = []
    import bisect
    for x in seq:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


# ---------- card 0: Erdos-Szekeres, permutations of 9 with no monotone 4-chain ----------
def card0():
    count9 = 0
    for p in itertools.permutations(range(9)):
        if lis_len(p) <= 3 and lis_len([-x for x in p]) <= 3:
            count9 += 1
    check(0, "perms of 9, LIS<=3 & LDS<=3", 1764, count9)
    check(0, "42^2", 1764, 42 * 42)
    # hook length formula for shape (3,3,3)
    hooks = [5, 4, 3, 4, 3, 2, 3, 2, 1]
    prod = 1
    for h in hooks:
        prod *= h
    f333 = factorial(9) // prod
    check(0, "f^(3,3,3) hook formula", 42, f333)
    # every permutation of 10 has a monotone subsequence of length 4 (Erdos-Szekeres)
    bad10 = 0
    for p in itertools.permutations(range(10)):
        if lis_len(p) <= 3 and lis_len([-x for x in p]) <= 3:
            bad10 += 1
    check(0, "perms of 10 avoiding monotone 4 (=0)", 0, bad10)


# ---------- card 1: five points in unit square, max min distance = sqrt(2)/2 ----------
def card1():
    pts = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(1, 2), F(1, 2))]
    min_sq = min((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
                 for a, b in itertools.combinations(pts, 2))
    check(1, "min squared distance corners+centre", F(1, 2), min_sq)
    check(1, "sqrt(2)/2 value", round(sqrt(2) / 2, 6), 0.707107, tol=1e-6)
    rng = random.Random(1)
    trials = 100000
    best = 0.0
    viol = 0
    for _ in range(trials):
        q = [(rng.random(), rng.random()) for _ in range(5)]
        m = min(math.dist(a, b) for a, b in itertools.combinations(q, 2))
        best = max(best, m)
        if m > sqrt(2) / 2 + 1e-12:
            viol += 1
    # pigeonhole argument: 5 points, 4 closed quadrants -> min distance <= sqrt(2)/2
    check(1, "random 5-point configs violating bound (1e5 trials)", 0, viol)
    check(1, "max observed min-dist <= sqrt(2)/2", 1, 1 if best <= sqrt(2) / 2 + 1e-12 else 0)
    print(f"        best observed min-dist over {trials} random trials = {best:.6f} (bound {sqrt(2)/2:.6f})")


# ---------- card 2: any 7 integers have zero-sum nonempty subset mod 7; 6 integers do not ----------
def zero_sum_subset_exists(residues, n):
    R = set()
    for x in residues:
        new = {(r + x) % n for r in R}
        new.add(x % n)
        R |= new
        if 0 in R:
            return True
    return 0 in R


def card2():
    n = 7
    all_ok = True
    for tup in itertools.product(range(n), repeat=n):
        if not zero_sum_subset_exists(tup, n):
            all_ok = False
            break
    check(2, "every 7-tuple mod 7 has zero-sum subset", 1, 1 if all_ok else 0)
    check(2, "all-ones 6-tuple has zero-sum subset (=0)", 0,
          1 if zero_sum_subset_exists([1] * 6, 7) else 0)
    free6 = sum(1 for tup in itertools.product(range(7), repeat=6)
                if not zero_sum_subset_exists(tup, 7))
    print(f"        zero-sum-free 6-tuples mod 7 (count, for info) = {free6}")
    check(2, "zero-sum-free 6-tuples exist", 1, 1 if free6 > 0 else 0)


# ---------- card 3: pairs {x,x+2} partition; max set avoiding difference 2 in 1..100 ----------
def max_indep_path_union(nodes_by_chain):
    """Max independent set on disjoint union of paths; each chain is a list of nodes in path order."""
    total = 0
    for chain in nodes_by_chain:
        a, b = 0, 1  # dp over path: best with last not taken (a), last taken (b)
        best_prev_not, best_prev_take = 0, 0
        first = True
        for _ in chain:
            if first:
                not_take, take = 0, 1
                first = False
            else:
                not_take = max(best_prev_not, best_prev_take)
                take = best_prev_not + 1
            best_prev_not, best_prev_take = not_take, take
        total += max(best_prev_not, best_prev_take)
    return total


def card3():
    # difference-2 conflict graph: two paths (odds and evens), each of length 50
    chains = [list(range(1, 101, 2)), list(range(2, 101, 2))]
    mis = max_indep_path_union(chains)
    check(3, "max set avoiding difference 2 in 1..100", 50, mis)
    check(3, "forced count = 50+1", 51, mis + 1)
    # explicit pair cover by {x,x+2} pairs: 50 pairs covering 1..100
    pairs = [(x, x + 2) for x in range(1, 100, 4)] + [(x, x + 2) for x in range(2, 100, 4)]
    covered = sorted(v for p in pairs for v in p)
    cover_ok = covered == list(range(1, 101)) and len(pairs) == 50
    check(3, "pair cover of 1..100 by 50 pairs differing by 2", 1, 1 if cover_ok else 0)
    # explicit 50-element set avoiding difference 2: pattern 1,2,5,6,9,10,...
    S = [x for x in range(1, 101) if x % 4 in (1, 2)]
    avoid = all((a + 2) not in set(S) for a in S)
    check(3, "explicit 50-set avoids difference 2", 1, 1 if (avoid and len(S) == 50) else 0)
    # difference 3 variant: three residue chains of lengths 34, 33, 33
    chains3 = [list(range(r, 101, 3)) for r in (1, 2, 3)]
    mis3 = max_indep_path_union(chains3)
    check(3, "difference-3 variant: max avoiding set", 51, mis3)


# ---------- card 4: 28 tickets forces four with same residue mod 9 ----------
def card4():
    tickets = range(1, 201)
    counts = {r: sum(1 for t in tickets if t % 9 == r) for r in range(9)}
    min_count = min(counts.values())
    check(4, "each residue class has >= 3 tickets in 1..200", 1, 1 if min_count >= 3 else 0)
    check(4, "largest safe draw = 9*3", 27, 9 * 3)
    check(4, "forced draw = 9*3+1", 28, 9 * 3 + 1)


# ---------- card 5: non-decreasing sequences length 5 in {1..8} ----------
def card5():
    cnt = sum(1 for _ in itertools.combinations_with_replacement(range(1, 9), 5))
    check(5, "non-decreasing sequences", 792, cnt)
    check(5, "C(12,5)", 792, comb(12, 5))
    # sample sequence (1,1,3,6,6) -> lattice path with 5 N and 7 E steps
    seq = (1, 1, 3, 6, 6)
    steps = []
    for v in range(1, 9):
        steps += ["N"] * seq.count(v)
        if v < 8:
            steps += ["E"]
    ok = steps.count("N") == 5 and steps.count("E") == 7 and len(steps) == 12
    check(5, "path encoding: 5 N, 7 E", 1, 1 if ok else 0)


# ---------- card 6: x1+..+x4=15, 2<=x_i<=7 ----------
def card6():
    cnt = 0
    for x in itertools.product(range(2, 8), repeat=4):
        if sum(x) == 15:
            cnt += 1
    check(6, "bounded solutions 2<=x_i<=7, sum 15", 104, cnt)
    check(6, "IE: C(10,3)-4*C(4,3)", 104, comb(10, 3) - 4 * comb(4, 3))


# ---------- card 7: x1 odd, x2,x3,x4 even, sum 21, non-negative ----------
def card7():
    cnt = 0
    for x in itertools.product(range(0, 22), repeat=4):
        if sum(x) == 21 and x[0] % 2 == 1 and all(v % 2 == 0 for v in x[1:]):
            cnt += 1
    check(7, "parity-constrained solutions", 286, cnt)
    check(7, "C(13,3)", 286, comb(13, 3))


# ---------- card 8: four dice sum 14 ----------
def card8():
    cnt = 0
    for x in itertools.product(range(1, 7), repeat=4):
        if sum(x) == 14:
            cnt += 1
    check(8, "four dice total 14", 146, cnt)
    check(8, "wrong solution C(13,3)", 286, comb(13, 3))
    check(8, "correct via IE: 286-4*C(7,3)", 146, comb(13, 3) - 4 * comb(7, 3))
    # the claimed faulty step: (10,0,0,0) is a non-die solution of y-sum 10
    check(8, "faulty L3: y=(10,0,0,0) violates y_i<=5", 1, 1 if 10 > 5 else 0)


# ---------- card 9: a+b+ab merge, invariant prod(1+x) ----------
def card9():
    finals = set()

    def rec(board):
        if len(board) == 1:
            finals.add(board[0])
            return
        for i, j in itertools.combinations(range(len(board)), 2):
            a, b = board[i], board[j]
            rest = [board[k] for k in range(len(board)) if k not in (i, j)]
            rec(rest + [a + b + a * b])

    rec([1, 2, 3, 4])
    check(9, "all merge orders give one value", 1, 1 if len(finals) == 1 else 0)
    check(9, "final value 119", 119, next(iter(finals)))
    check(9, "prod(1+x) = 120 so x = 119", 119, 2 * 3 * 4 * 5 - 1)


# ---------- card 10: 15-puzzle reachable fraction ----------
def bfs_reachable(rows, cols):
    n = rows * cols
    start = tuple(list(range(1, n)) + [0])
    seen = {start}
    dq = deque([start])
    while dq:
        s = dq.popleft()
        z = s.index(0)
        r, c = divmod(z, cols)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                t = list(s)
                w = nr * cols + nc
                t[z], t[w] = t[w], t[z]
                t = tuple(t)
                if t not in seen:
                    seen.add(t)
                    dq.append(t)
    return len(seen)


def card10():
    for rows, cols in ((2, 2), (2, 3), (2, 4), (3, 3)):
        n = rows * cols
        reach = bfs_reachable(rows, cols)
        check(10, f"BFS {rows}x{cols}: reachable/(n!) = 1/2", F(1, 2), F(reach, factorial(n)))
    check(10, "16!/2 count", 10461394944000, factorial(16) // 2)
    check(10, "16!/2 is exactly half of 16!", factorial(16), 2 * (factorial(16) // 2))
    # invariant on 4x4: inv(tile sequence, blank removed) + row of blank (1-indexed) mod 2
    rng = random.Random(3)
    state = list(range(1, 16)) + [0]

    def inv_quantity(s):
        seq = [v for v in s if v != 0]
        inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])
        blank_row = s.index(0) // 4 + 1
        return (inv + blank_row) % 2

    q0 = inv_quantity(state)
    constant = True
    for _ in range(100000):
        z = state.index(0)
        r, c = divmod(z, 4)
        moves = []
        if r > 0: moves.append(z - 4)
        if r < 3: moves.append(z + 4)
        if c > 0: moves.append(z - 1)
        if c < 3: moves.append(z + 1)
        w = rng.choice(moves)
        state[z], state[w] = state[w], state[z]
        if inv_quantity(state) != q0:
            constant = False
            break
    check(10, "4x4 invariant constant over 1e5 random slides", 1, 1 if constant else 0)
    swap = list(range(1, 16)) + [0]
    swap[13], swap[14] = swap[14], swap[13]
    check(10, "14<->15 swap has different invariant (unsolvable)", 1,
          1 if inv_quantity(swap) != inv_quantity(list(range(1, 16)) + [0]) else 0)


# ---------- card 11: 8x8 minus a corner by L-trominoes; 21 trominoes ----------
def l_tromino_tilings(cells):
    """Backtracking exact cover of a set of cells by L-trominoes. Returns list of pieces or None."""
    cells = set(cells)
    order = sorted(cells)
    placed = []

    def pieces_covering(first):
        r, c = first
        out = []
        for br in (r - 1, r):
            for bc in (c - 1, c):
                block = [(br, bc), (br, bc + 1), (br + 1, bc), (br + 1, bc + 1)]
                for skip in block:
                    piece = [q for q in block if q != skip]
                    if first in piece and all(q in cells for q in piece):
                        if len(piece) == 3 and set(piece) <= cells:
                            out.append(tuple(sorted(piece)))
        return list({p for p in out})

    def solve(remaining):
        if not remaining:
            return True
        first = min(remaining)
        for piece in pieces_covering(first):
            if set(piece) <= remaining:
                placed.append(piece)
                if solve(remaining - set(piece)):
                    return True
                placed.pop()
        return False

    ok = solve(cells)
    return list(placed) if ok else None


def card11():
    # domino colour argument on 8x8 minus two corners (a1, h8): 30 black vs 32 white
    black = [(r, c) for r in range(8) for c in range(8) if (r + c) % 2 == 0]
    white = [(r, c) for r in range(8) for c in range(8) if (r + c) % 2 == 1]
    removed = {(0, 0), (7, 7)}
    b_left = sum(1 for q in black if q not in removed)
    w_left = sum(1 for q in white if q not in removed)
    check(11, "domino colour counts after removing a1,h8 (black)", 30, b_left)
    check(11, "domino colour counts after removing a1,h8 (white)", 32, w_left)
    # L-tromino tiling of 8x8 minus one corner, 21 pieces
    board = {(r, c) for r in range(8) for c in range(8)} - {(0, 0)}
    tiles = l_tromino_tilings(board)
    check(11, "8x8 minus corner tiled by L-trominoes (1 = found)", 1, 1 if tiles else 0)
    check(11, "number of L-trominoes = 63/3", 21, len(board) // 3)
    if tiles:
        covered = [q for p in tiles for q in p]
        check(11, "tiling covers board exactly once", 1,
              1 if sorted(covered) == sorted(board) else 0)
    # 4x4 minus corner: explicit 5-tromino tiling used on the figure and in the induction
    four = {(r, c) for r in range(4) for c in range(4)} - {(3, 0)}
    expl = [((0, 0), (0, 1), (1, 0)), ((0, 2), (0, 3), (1, 3)), ((2, 3), (3, 2), (3, 3)),
            ((2, 0), (2, 1), (3, 1)), ((1, 1), (1, 2), (2, 2))]
    cov = sorted(q for p in expl for q in p)
    check(11, "explicit 4x4-minus-corner tiling covers exactly", 1,
          1 if cov == sorted(four) else 0)
    check(11, "4x4 minus corner uses 5 trominoes", 5, len(expl))


# ---------- card 12: lamp xor invariant, reachable fraction and lamp-1 test ----------
def card12():
    n = 10
    buttons = []
    for i in range(8):
        v = 0
        for j in (i, i + 1, i + 2):
            v |= 1 << j
        buttons.append(v)
    span = {0}
    for b in buttons:
        span |= {s ^ b for s in span}
    check(12, "reachable patterns = 2^8", 256, len(span))
    check(12, "reachable fraction", F(1, 4), F(len(span), 2 ** n))
    c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    cmask = sum(bit << j for j, bit in enumerate(c))

    def weight_parity(x):
        return bin(x & cmask).count("1") % 2

    inv_ok = all(weight_parity(b) == 0 for b in buttons)
    check(12, "weight invariant preserved by every button", 1, 1 if inv_ok else 0)
    lamp1 = 1 << 0
    check(12, "lamp 1 alone is NOT reachable", 0, 1 if lamp1 in span else 0)
    check(12, "weight of lamp 1 alone is 1", 1, weight_parity(lamp1))


# ---------- card 13: product mod 7 invariant, final label ----------
def card13():
    finals = set()

    def rec(board):
        if len(board) == 1:
            finals.add(board[0])
            return
        for i, j in itertools.combinations(range(len(board)), 2):
            rest = [board[k] for k in range(len(board)) if k not in (i, j)]
            rec(rest + [(board[i] * board[j]) % 7])

    rec([1, 2, 3, 4, 5, 6])
    check(13, "all merge orders give the same label", 1, 1 if len(finals) == 1 else 0)
    check(13, "final label", 6, next(iter(finals)))
    check(13, "6! mod 7 = 6 (Wilson)", 6, factorial(6) % 7)
    check(13, "sum-version final label would be 21 mod 7", 0, 21 % 7)


# ---------- card 14: adjacent swaps on reversed 10 items use exactly 45 swaps ----------
def card14():
    rng = random.Random(5)
    trials = 100000
    counts = []
    for _ in range(trials):
        a = list(range(10, 0, -1))
        steps = 0
        while True:
            bad = [i for i in range(9) if a[i] > a[i + 1]]
            if not bad:
                break
            i = rng.choice(bad)
            a[i], a[i + 1] = a[i + 1], a[i]
            steps += 1
        counts.append(steps)
    mean = sum(counts) / trials
    var = sum((x - mean) ** 2 for x in counts) / (trials - 1)
    se = math.sqrt(var / trials)
    print(f"        adjacent-swap steps over {trials} random sorts: mean={mean:.6f} SE={se:.2e}")
    check(14, "swaps needed to sort reversed 10 items (all runs)", 45, 45 if all(x == 45 for x in counts) else -1)
    check(14, "C(10,2)", 45, comb(10, 2))


def json_consistency():
    """Each claimed answer must appear in its card's back in staging/gap_A.json."""
    import json
    import os
    import re
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gap_A.json")
    with open(path, encoding="utf-8") as fh:
        cards = json.load(fh)
    expected = {0: ["1764"], 1: [r"sqrt2}{2}"], 2: ["1,1,1,1,1,1"], 3: ["50", "51"],
                4: ["28"], 5: ["792"], 6: ["104"], 7: ["286"], 8: ["146", "286"], 9: ["119"],
                10: ["16!/2", "10\\,461"], 11: ["21"], 12: ["256"], 13: ["6."], 14: ["45"]}
    for idx, needles in expected.items():
        back = re.sub(r"\s+", " ", cards[idx]["back"]) + " " + cards[idx]["front"]
        for nd in needles:
            ok = nd in back
            RESULTS.append(ok)
            print(f"card {idx:2d} [JSON contains {nd!r}] {'PASS' if ok else 'FAIL'}")
    RESULTS.append(len(cards) == 15)
    print(f"card --  [JSON has 15 cards] claimed=15 computed={len(cards)} {'PASS' if len(cards) == 15 else 'FAIL'}")


def main():
    for f in (card0, card1, card2, card3, card4, card5, card6, card7, card8, card9,
              card10, card11, card12, card13, card14):
        f()
    json_consistency()
    npass = sum(RESULTS)
    print(f"SUMMARY: {npass}/{len(RESULTS)} checks PASS")
    if npass != len(RESULTS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
