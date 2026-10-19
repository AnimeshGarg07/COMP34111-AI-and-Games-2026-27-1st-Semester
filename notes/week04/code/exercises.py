"""Check the handout exercises and the game facts used in the Week 4 notes."""
from functools import lru_cache
from itertools import product

# ---------------------------------------------------------------------------
# 1. Minimax handout, Exercise 1 (Figure 4): non-zero-sum game, pay-offs (P1, P2)
# ---------------------------------------------------------------------------
def leaf(p):
    return ("leaf", p)

fig4 = ("P1", "root", [
    ("P2", "X", [leaf((4, 3)),
                 ("P1", "Y1", [leaf((1, -1)), leaf((2, -2))]),
                 ("P1", "Y2", [leaf((-1, 3)), leaf((2, -2)), leaf((1, 2))])]),
    leaf((-1, 4)),
    ("P2", "Z", [leaf((2, 3)), leaf((-2, 4))]),
])


def value_for(node, i, choices):
    """Minimax value for player i (0 or 1): max at i's nodes, min at the other's."""
    if node[0] == "leaf":
        return node[1][i]
    who, name, ch = node
    vals = [value_for(c, i, choices) for c in ch]
    me = ("P1", "P2")[i]
    v = max(vals) if who == me else min(vals)
    if who == me:
        choices[name] = [k for k, x in enumerate(vals) if x == v]
    return v


def backward_induction(node, choices):
    """Each mover maximises their OWN pay-off (subgame-perfect play)."""
    if node[0] == "leaf":
        return node[1]
    who, name, ch = node
    i = 0 if who == "P1" else 1
    outs = [backward_induction(c, choices) for c in ch]
    best = max(o[i] for o in outs)
    choices[name] = [k for k, o in enumerate(outs) if o[i] == best]
    return outs[choices[name][0]]


def play(node, strat):
    if node[0] == "leaf":
        return node[1]
    who, name, ch = node
    return play(ch[strat[name]], strat)


c1, c2 = {}, {}
v1 = value_for(fig4, 0, c1)
v2 = value_for(fig4, 1, c2)
print("Fig4: value for P1 =", v1, "choices", c1)
print("Fig4: value for P2 =", v2, "choices", c2)
strat = {k: v[0] for k, v in {**c1, **c2}.items()}
print("Fig4: both play security strategies ->", play(fig4, strat))
bi = {}
print("Fig4: backward induction outcome", backward_induction(fig4, bi), bi)

# ---------------------------------------------------------------------------
# 2. Alpha-beta handout exercise: 2x3 Chomp and (3,3,3)-Nim
# ---------------------------------------------------------------------------
# Chomp position = tuple of row lengths, bottom row first, non-increasing.
# Poison = bottom-left square. Choosing square (r, c) removes all squares
# (r', c') with r' >= r and c' >= c. Whoever takes the poison loses, so a
# player facing only the poison (1,) or (1,0) has lost.

def chomp_moves(pos):
    rows = list(pos)
    for r in range(len(rows)):
        for c in range(rows[r]):
            if r == 0 and c == 0:
                continue  # eating the poison = losing; treat as no legal move
            new = [min(rows[k], c) if k >= r else rows[k] for k in range(len(rows))]
            yield (r, c), tuple(new)


@lru_cache(None)
def chomp_win(pos):
    """True if the player to move wins (opponent eventually must eat poison)."""
    return any(not chomp_win(p) for _, p in chomp_moves(pos))


start = (3, 3)
wins = [(m, p) for m, p in chomp_moves(start) if not chomp_win(p)]
print("2x3 Chomp: first player wins?", chomp_win(start), " winning first moves:", wins)
for pos in sorted({p for _, p in chomp_moves(start)} | {(3, 2), (2, 1), (1, 0), (3, 1), (2, 2), (2, 0), (3, 0), (1, 1)}):
    print("   position", pos, "to-move wins" if chomp_win(pos) else "to-move LOSES")


def nim_moves(h):
    for i, x in enumerate(h):
        for take in range(1, x + 1):
            n = list(h)
            n[i] -= take
            yield (i, take), tuple(sorted(n))


@lru_cache(None)
def nim_win(h, misere):
    if sum(h) == 0:
        # no move possible: in normal play the player to move has lost
        # (opponent took last); in misere play the player to move has won.
        return misere
    return any(not nim_win(p, misere) for _, p in nim_moves(h))


for mis in (False, True):
    h = (3, 3, 3)
    w = sorted({p for m, p in nim_moves(h) if not nim_win(p, mis)})
    print(f"(3,3,3)-Nim {'misere' if mis else 'normal'}: first wins? {nim_win(h, mis)}; winning replies lead to {w}")

# count game-tree size for (3,3,3) Nim and 2x3 Chomp
@lru_cache(None)
def nim_tree_size(h):
    if sum(h) == 0:
        return 1
    return 1 + sum(nim_tree_size(p) for _, p in nim_moves(h))


@lru_cache(None)
def chomp_tree_size(p):
    return 1 + sum(chomp_tree_size(q) for _, q in chomp_moves(p))


print("nodes in full (3,3,3)-Nim tree (sorted heaps, not merging transpositions):", nim_tree_size((3, 3, 3)))
print("nodes in full 2x3 Chomp tree:", chomp_tree_size((3, 3)))

# ---------------------------------------------------------------------------
# 3. Tic-tac-toe facts
# ---------------------------------------------------------------------------
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != "." and b[a] == b[c] == b[d]:
            return b[a]
    return None


games = 0
positions = set()
def walk(b, p):
    global games
    positions.add(b)
    if winner(b) or "." not in b:
        games += 1
        return
    for k in range(9):
        if b[k] == ".":
            walk(b[:k] + p + b[k + 1:], "O" if p == "X" else "X")


walk("." * 9, "X")
print("tic-tac-toe complete games:", games, " reachable positions:", len(positions))


@lru_cache(None)
def n_strategies(b, p, me):
    """Number of (reduced) pure strategies for player `me` in the subtree."""
    if winner(b) or "." not in b:
        return 1
    kids = [b[:k] + p + b[k + 1:] for k in range(9) if b[k] == "."]
    nxt = "O" if p == "X" else "X"
    if p == me:
        return sum(n_strategies(c, nxt, me) for c in kids)
    out = 1
    for c in kids:
        out *= n_strategies(c, nxt, me)
    return out


sx = n_strategies("." * 9, "X", "X")
so = n_strategies("." * 9, "X", "O")
print("reduced strategies for X: %d (about 10^%d)" % (sx, len(str(sx)) - 1))
print("reduced strategies for O: about 10^%d" % (len(str(so)) - 1))


def h_open_lines(b):
    """(lines with no O) - (lines with no X): open lines for X minus open lines for O."""
    x_open = sum(1 for l in LINES if all(b[k] != "O" for k in l))
    o_open = sum(1 for l in LINES if all(b[k] != "X" for k in l))
    return x_open, o_open, x_open - o_open


def board(xs, os_):
    b = ["."] * 9
    for k in xs:
        b[k] = "X"
    for k in os_:
        b[k] = "O"
    return "".join(b)


# squares: a b c / d e f / g h i  -> 0..8
sq = {ch: i for i, ch in enumerate("abcdefghi")}
print("Depth-2 tic-tac-toe (Duke figure):")
for xmove, replies in (("a", "dghie"), ("d", "abcfe"), ("e", "ad")):
    vals = []
    for o in replies:
        xo, oo, h = h_open_lines(board([sq[xmove]], [sq[o]]))
        vals.append(h)
        print(f"   X at {xmove}, O at {o}: {xo}-{oo}={h}")
    print(f"   -> MIN node value {min(vals)}")

# Slide 14 sequence
for xs, os_ in (("ce", "f"), ("ce", "fg"), ("ace", "fg")):
    xo, oo, h = h_open_lines(board([sq[c] for c in xs], [sq[c] for c in os_]))
    print(f"slide-14 board X={xs} O={os_}: {xo}-{oo}={h}")


@lru_cache(None)
def ttt_value(b, p):
    w = winner(b)
    if w == "X":
        return 1
    if w == "O":
        return -1
    if "." not in b:
        return 0
    nxt = "O" if p == "X" else "X"
    vals = [ttt_value(b[:k] + p + b[k + 1:], nxt) for k in range(9) if b[k] == "."]
    return max(vals) if p == "X" else min(vals)


print("true value of slide-14 boards (X=+1):",
      ttt_value(board([2, 4], [5]), "O"), ttt_value(board([2, 4], [5, 6]), "X"), ttt_value(board([0, 2, 4], [5, 6]), "O"))
print("true value of empty board:", ttt_value("." * 9, "X"))

# ---------------------------------------------------------------------------
# 4. Connect-4: number of possible winning lines on 7x6
# ---------------------------------------------------------------------------
R, C = 6, 7
lines = 0
for r in range(R):
    for c in range(C):
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            if 0 <= r + 3 * dr < R and 0 <= c + 3 * dc < C:
                lines += 1
print("Connect-4 winning lines:", lines)

# ---------------------------------------------------------------------------
# 5. Othello board on slides 21-25 (row 1 = top, columns a..h)
# ---------------------------------------------------------------------------
rows = [
    "....W...",
    "....W...",
    "W.BWWB..",
    "WWBBWB..",
    "WWWWWB..",
    "..BWBB..",
    "...BWB..",
    "BBBBBB..",
]
grid = [list(r) for r in rows]
DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def legal(grid, me):
    opp = "W" if me == "B" else "B"
    out = []
    for r in range(8):
        for c in range(8):
            if grid[r][c] != ".":
                continue
            flips = 0
            for dr, dc in DIRS:
                rr, cc, n = r + dr, c + dc, 0
                while 0 <= rr < 8 and 0 <= cc < 8 and grid[rr][cc] == opp:
                    rr += dr
                    cc += dc
                    n += 1
                if n and 0 <= rr < 8 and 0 <= cc < 8 and grid[rr][cc] == me:
                    flips += n
            if flips:
                out.append(("abcdefgh"[c] + str(r + 1), flips))
    return out


nb = sum(r.count("B") for r in rows)
nw = sum(r.count("W") for r in rows)
corners = {"a1": grid[0][0], "h1": grid[0][7], "a8": grid[7][0], "h8": grid[7][7]}
mb, mw = legal(grid, "B"), legal(grid, "W")
print(f"Othello: black {nb}, white {nw}; corners {corners}")
print(f"   black legal moves ({len(mb)}): {mb}")
print(f"   white legal moves ({len(mw)}): {mw}")


def rel(a, b):
    return 100 * (a - b) / (a + b) if a + b else 0


print(f"   parity (black view) {rel(nb, nw):.1f}; mobility {rel(len(mb), len(mw)):.1f}")
