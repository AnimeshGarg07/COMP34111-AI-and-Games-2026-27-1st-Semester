"""Game trees from the Week 4 slides, with minimax and traced alpha-beta.

A node is a dict: {"name", "type": "max"|"min"|"leaf", "value" (leaves), "children"}.
"""
import math

INF = math.inf


def L(v, name=None):
    return {"type": "leaf", "value": v, "name": name, "children": []}


def MAX(name, *ch):
    return {"type": "max", "name": name, "children": list(ch)}


def MIN(name, *ch):
    return {"type": "min", "name": name, "children": list(ch)}


def minimax(n):
    if n["type"] == "leaf":
        n["mm"] = n["value"]
        return n["value"]
    vals = [minimax(c) for c in n["children"]]
    n["mm"] = max(vals) if n["type"] == "max" else min(vals)
    return n["mm"]


def fmt(x):
    if x == INF:
        return "+inf"
    if x == -INF:
        return "-inf"
    return str(x)


def alphabeta(n, a=-INF, b=INF, trace=None, depth=0, visited=None):
    """Standard fail-hard alpha-beta following the Lecture 6 update table.

    Records the window each node is entered with, and marks visited nodes.
    """
    n["window_in"] = (a, b)
    n["visited"] = True
    if visited is not None and n["type"] == "leaf":
        visited.append(n["value"])
    if n["type"] == "leaf":
        if trace is not None:
            trace.append(f"{'  '*depth}leaf {n['value']}")
        return n["value"]
    if trace is not None:
        trace.append(f"{'  '*depth}enter {n['type'].upper()} {n['name']} with [{fmt(a)}, {fmt(b)}]")
    for i, c in enumerate(n["children"]):
        v = alphabeta(c, a, b, trace, depth + 1, visited)
        if n["type"] == "max":
            if v >= b:
                if trace is not None:
                    trace.append(f"{'  '*depth}{n['name']}: v={fmt(v)} >= beta={fmt(b)} -> CUTOFF, prune {len(n['children'])-i-1} remaining child(ren)")
                n["cut_after"] = i
                n["ab"] = v
                return v
            if v > a:
                a = v
                if trace is not None:
                    trace.append(f"{'  '*depth}{n['name']}: alpha := {fmt(a)}")
        else:
            if v <= a:
                if trace is not None:
                    trace.append(f"{'  '*depth}{n['name']}: v={fmt(v)} <= alpha={fmt(a)} -> CUTOFF, prune {len(n['children'])-i-1} remaining child(ren)")
                n["cut_after"] = i
                n["ab"] = v
                return v
            if v < b:
                b = v
                if trace is not None:
                    trace.append(f"{'  '*depth}{n['name']}: beta := {fmt(b)}")
        n["window_now"] = (a, b)
    r = a if n["type"] == "max" else b
    n["ab"] = r
    if trace is not None:
        trace.append(f"{'  '*depth}return {n['name']} = {fmt(r)}")
    return r


def shapiro_evaluate(n, a=-INF, b=INF, visited=None):
    """Literal reading of the Lecture 7 slide-7 pseudo-code (first child sets alpha/beta)."""
    if n["type"] == "leaf":
        if visited is not None:
            visited.append(n["value"])
        return n["value"]
    for i, c in enumerate(n["children"]):
        v = shapiro_evaluate(c, a, b, visited)
        if n["type"] == "max":
            a = v if i == 0 else max(a, v)
        else:
            b = v if i == 0 else min(b, v)
        if b <= a:
            break
    return a if n["type"] == "max" else b


def count_leaves(n):
    if n["type"] == "leaf":
        return 1
    return sum(count_leaves(c) for c in n["children"])


def pruned_nodes(n, acc=None):
    if acc is None:
        acc = []
    for c in n["children"]:
        if not c.get("visited"):
            acc.append(c.get("name") or f"leaf {c['value']}")
        else:
            pruned_nodes(c, acc)
    return acc


# ---- Lecture 5 (Sun) example tree: slides 13, 16-17 ----
def l5_tree():
    return MAX("root",
               MIN("A", L(4), MAX("B1", L(1), L(2)), MAX("B2", L(-1), L(2), L(1))),
               L(-1),
               MIN("C", L(2), L(-2)))


# ---- Lecture 7 (Shapiro) worked example 1: slide 8 ----
def l7_ex1():
    return MAX("Root",
               MIN("C1", L(2), MAX("2.1", L(3), MIN("3.1", L(-3)))),
               MIN("C2", L(-3), MAX("2.2", L(3))),
               MIN("C3", L(3), MAX("2.3", L(4))))


# ---- Lecture 7 (Shapiro) worked example 2: slide 9 ----
def l7_ex2():
    return MAX("Root",
               MIN("C1", L(-3), MAX("2.1", L(4), MIN("3.1", MAX("4.1", L(-13), L(10)), MAX("4.2", L(12), L(-12))))),
               MIN("C2", MAX("2.2", MIN("3.2", L(-13), L(-10)))),
               MIN("C3", L(4), MAX("2.3", L(5), MIN("3.3", MAX("4.3", L(-4), L(-3)), MAX("4.4", L(6), L(5))))))


def report(name, t):
    print("=" * 70)
    print(name)
    print("minimax value:", minimax(t), " leaves:", count_leaves(t))
    tr, vis = [], []
    v = alphabeta(t, trace=tr, visited=vis)
    print("alpha-beta value:", v, " leaves visited:", len(vis), vis)
    print("pruned subtrees:", pruned_nodes(t))
    for line in tr:
        print(line)
    vis2 = []
    print("Shapiro literal pseudo-code value:", shapiro_evaluate(t, visited=vis2), "leaves:", vis2)


if __name__ == "__main__":
    report("Lecture 5 tree", l5_tree())
    report("Lecture 7 example 1", l7_ex1())
    report("Lecture 7 example 2", l7_ex2())
