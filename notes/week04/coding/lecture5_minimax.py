"""Lecture 5 in code: minimax on explicit trees, chance nodes, non-zero-sum games,
and on an implicit game (tic-tac-toe) given only by its rules."""
from dataclasses import dataclass, field
from functools import lru_cache
import time


# ---------------------------------------------------------------- 1. explicit trees
@dataclass
class Node:
    kind: str                      # "max", "min", "chance" or "leaf"
    payoff: float = 0.0            # used only by leaves
    children: list = field(default_factory=list)
    probs: list = field(default_factory=list)   # used only by chance nodes
    name: str = ""


def leaf(v, name=""):
    return Node("leaf", payoff=v, name=name)


def MAX(name, *ch):
    return Node("max", children=list(ch), name=name)


def MIN(name, *ch):
    return Node("min", children=list(ch), name=name)


def CHANCE(name, pairs):
    return Node("chance", children=[c for _, c in pairs], probs=[p for p, _ in pairs], name=name)


def minimax(node):
    """Slide 7's rule, recursively (depth-first)."""
    if node.kind == "leaf":
        return node.payoff
    values = [minimax(c) for c in node.children]
    if node.kind == "max":
        return max(values)
    if node.kind == "min":
        return min(values)
    return sum(p * v for p, v in zip(node.probs, values))       # chance node


def lecture5_tree():
    return MAX("root",
               MIN("A", leaf(4), MAX("B1", leaf(1), leaf(2)), MAX("B2", leaf(-1), leaf(2), leaf(1))),
               leaf(-1),
               MIN("C", leaf(2), leaf(-2)))


# ---------------------------------------------------------------- 2. tracing the search
def minimax_traced(node, depth=0, log=None):
    """Same algorithm, printing when each node is entered and when its value is final."""
    pad = "    " * depth
    if node.kind == "leaf":
        log.append(f"{pad}leaf {node.payoff}")
        return node.payoff
    log.append(f"{pad}enter {node.kind.upper()} {node.name}")
    values = [minimax_traced(c, depth + 1, log) for c in node.children]
    v = max(values) if node.kind == "max" else min(values)
    log.append(f"{pad}{node.name} = {node.kind}{tuple(values)} = {v}")
    return v


# ---------------------------------------------------------------- 3. bottom-up, for contrast
def bottom_up(root):
    """Collect the whole tree level by level, then evaluate from the deepest level up."""
    levels, frontier = [], [root]
    while frontier:                                   # needs every node in memory at once
        levels.append(frontier)
        frontier = [c for n in frontier for c in n.children]
    value = {}
    for level in reversed(levels):
        for n in level:
            if n.kind == "leaf":
                value[id(n)] = n.payoff
            else:
                vs = [value[id(c)] for c in n.children]
                value[id(n)] = max(vs) if n.kind == "max" else min(vs)
    return value[id(root)], sum(len(l) for l in levels)


# ---------------------------------------------------------------- 4. values -> strategies
def solve(node, strategy):
    """Return the value, and record the best child's name at every MAX/MIN node."""
    if node.kind == "leaf":
        return node.payoff
    values = [solve(c, strategy) for c in node.children]
    best = max(values) if node.kind == "max" else min(values)
    strategy[node.name] = [c.name or f"leaf {c.payoff}" for c, v in zip(node.children, values) if v == best]
    return best


# ---------------------------------------------------------------- 5. non-zero-sum: run once per player
@dataclass
class GNode:
    player: int                    # 0 or 1 moves here; ignored for leaves
    name: str = ""
    children: list = field(default_factory=list)
    payoffs: tuple = None          # (P1, P2) at leaves


def value_for(node, i, choice):
    """Minimax for player i: max at i's nodes, min at the other player's nodes."""
    if node.payoffs is not None:
        return node.payoffs[i]
    vals = [value_for(c, i, choice) for c in node.children]
    if node.player == i:
        v = max(vals)
        choice[node.name] = vals.index(v)
        return v
    return min(vals)


def play(node, choice):
    while node.payoffs is None:
        node = node.children[choice[node.name]]
    return node.payoffs


def exercise_tree():
    L = lambda a, b: GNode(-1, payoffs=(a, b))
    return GNode(0, "root", [
        GNode(1, "X", [L(4, 3), GNode(0, "Y1", [L(1, -1), L(2, -2)]), GNode(0, "Y2", [L(-1, 3), L(2, -2), L(1, 2)])]),
        L(-1, 4),
        GNode(1, "Z", [L(2, 3), L(-2, 4)])])


# ---------------------------------------------------------------- 6. an implicit game: tic-tac-toe
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


class TicTacToe:
    """The game is given by rules, not by a stored tree: board = 9-char string, X moves first."""
    start = "........."

    @staticmethod
    def to_move(b):
        return "X" if b.count("X") == b.count("O") else "O"

    @staticmethod
    def winner(b):
        for i, j, k in LINES:
            if b[i] != "." and b[i] == b[j] == b[k]:
                return b[i]
        return None

    @classmethod
    def is_final(cls, b):
        return cls.winner(b) is not None or "." not in b

    @classmethod
    def payoff(cls, b):                     # to X (Player 1, MAX)
        return {"X": 1, "O": -1, None: 0}[cls.winner(b)]

    @staticmethod
    def moves(b):
        return [i for i, c in enumerate(b) if c == "."]

    @classmethod
    def play(cls, b, m):
        return b[:m] + cls.to_move(b) + b[m + 1:]


nodes_visited = 0


def minimax_game(game, s):
    global nodes_visited
    nodes_visited += 1
    if game.is_final(s):
        return game.payoff(s)
    values = [minimax_game(game, game.play(s, m)) for m in game.moves(s)]
    return max(values) if game.to_move(s) == "X" else min(values)


def best_move(game, s):
    pick = max if game.to_move(s) == "X" else min
    return pick(game.moves(s), key=lambda m: minimax_game(game, game.play(s, m)))


@lru_cache(maxsize=None)
def minimax_memo(s):
    """Same search, but each distinct position is solved once (a 'transposition table')."""
    g = TicTacToe
    if g.is_final(s):
        return g.payoff(s)
    values = [minimax_memo(g.play(s, m)) for m in g.moves(s)]
    return max(values) if g.to_move(s) == "X" else min(values)


# ---------------------------------------------------------------- 7. counting strategies (slide 2)
@lru_cache(maxsize=None)
def n_strategies(s, me):
    g = TicTacToe
    if g.is_final(s):
        return 1
    kids = [g.play(s, m) for m in g.moves(s)]
    if g.to_move(s) == me:
        return sum(n_strategies(k, me) for k in kids)
    out = 1
    for k in kids:
        out *= n_strategies(k, me)
    return out


if __name__ == "__main__":
    t = lecture5_tree()
    print("1. value of the Lecture 5 tree:", minimax(t))
    log = []
    minimax_traced(t, log=log)
    print("2. depth-first trace:\n" + "\n".join(log))
    print("3. bottom-up value and nodes held in memory:", bottom_up(t))
    strat = {}
    print("4. value", solve(t, strat), "best choices", strat)
    gamble = MAX("root", leaf(1, "safe"), CHANCE("coin", [(0.5, leaf(4)), (0.5, leaf(-1))]))
    oppon = MAX("root", leaf(1, "safe"), MIN("opp", leaf(4), leaf(-1)))
    print("   chance version:", minimax(gamble), " opponent version:", minimax(oppon))
    c1, c2 = {}, {}
    ex = exercise_tree()
    print("5. exercise: value P1 =", value_for(ex, 0, c1), "value P2 =", value_for(ex, 1, c2),
          "played:", play(ex, {**c1, **c2}))
    g = TicTacToe
    t0 = time.perf_counter(); v = minimax_game(g, g.start); t1 = time.perf_counter()
    print(f"6. tic-tac-toe value {v}, nodes visited {nodes_visited:,}, {t1 - t0:.2f} s")
    t0 = time.perf_counter(); v = minimax_memo(g.start); t1 = time.perf_counter()
    print(f"   with memo: value {v}, distinct positions solved {minimax_memo.cache_info().currsize:,}, {t1 - t0:.3f} s")
    print("   best reply to X in a corner:", best_move(g, "X........"))
    print("7. strategies for X: about 10^%d" % (len(str(n_strategies(g.start, "X"))) - 1))
