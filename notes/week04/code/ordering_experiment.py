"""How many leaves does alpha-beta look at? Uniform random trees, three move orderings."""
import json
import math
import sys

import numpy as np

sys.setrecursionlimit(10000)


def build(b, d, rng):
    """values[k] = minimax value of every node at level k (level d = leaves), root MAX."""
    leaves = rng.random(b ** d)
    values = [None] * (d + 1)
    values[d] = leaves
    for k in range(d - 1, -1, -1):
        child = values[k + 1].reshape(-1, b)
        values[k] = child.max(axis=1) if k % 2 == 0 else child.min(axis=1)
    return values


def alphabeta_count(values, b, d, order):
    count = 0

    def rec(k, i, a, beta):
        nonlocal count
        if k == d:
            count += 1
            return values[d][i]
        kids = list(range(i * b, i * b + b))
        is_max = k % 2 == 0
        if order == "perfect":
            kids.sort(key=lambda j: values[k + 1][j], reverse=is_max)
        elif order == "worst":
            kids.sort(key=lambda j: values[k + 1][j], reverse=not is_max)
        for j in kids:
            v = rec(k + 1, j, a, beta)
            if is_max:
                if v >= beta:
                    return v
                a = max(a, v)
            else:
                if v <= a:
                    return v
                beta = min(beta, v)
        return a if is_max else beta

    rec(0, 0, -math.inf, math.inf)
    return count


def knuth_moore(b, d):
    return b ** math.ceil(d / 2) + b ** math.floor(d / 2) - 1


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    rng = np.random.default_rng(34111)
    rows = []
    for d in range(1, dmax + 1):
        trials = 30 if d <= 6 else (10 if d <= 8 else 4)
        res = {"random": [], "perfect": [], "worst": []}
        for _ in range(trials):
            vals = build(b, d, rng)
            for o in res:
                res[o].append(alphabeta_count(vals, b, d, o))
        row = {
            "depth": d,
            "minimax": b ** d,
            "random_mean": float(np.mean(res["random"])),
            "perfect_mean": float(np.mean(res["perfect"])),
            "worst_mean": float(np.mean(res["worst"])),
            "knuth_moore": knuth_moore(b, d),
            "trials": trials,
        }
        rows.append(row)
        print(row, flush=True)
    json.dump({"b": b, "rows": rows}, open(f"ordering_b{b}.json", "w"), indent=1)
