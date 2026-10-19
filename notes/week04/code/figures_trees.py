"""Week 4 tree figures (SVG)."""
import os

from svgtree import C, Node, board, draw_tree, legend_items, num, svg_doc, text

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)


def save(name, body, w, h, title):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg_doc(body, w, h, title))


def panel_title(x, y, s, sub=""):
    out = [text(x, y, s, size=14, weight=700, anchor="start")]
    if sub:
        out.append(text(x, y + 18, sub, size=12, fill=C["ink2"], anchor="start"))
    return "\n".join(out)


LEAF = lambda v, **k: Node("leaf", str(v), **k)


# ---------------------------------------------------------------------------
# Figure 1: bottom-up storyboard on the Lecture 5 tree
# ---------------------------------------------------------------------------
def l5_tree(stage):
    """stage 0: leaves only; 1: bottom max nodes + C; 2: A; 3: root."""
    b1 = Node("max", "2" if stage >= 1 else "?", [LEAF(1), LEAF(2, edge="pv" if stage >= 3 else "normal")], name="B1", halo=stage == 1)
    b2 = Node("max", "2" if stage >= 1 else "?", [LEAF(-1), LEAF(2), LEAF(1)], name="B2", halo=stage == 1)
    a = Node("min", "2" if stage >= 2 else "?", [LEAF(4), b1, b2], name="A", halo=stage == 2,
             edge="pv" if stage >= 3 else "normal")
    if stage >= 3:
        b1.edge = "pv"
    c = Node("min", "−2" if stage >= 1 else "?", [LEAF(2), LEAF(-2)], name="C", halo=stage == 1)
    return Node("max", "2" if stage >= 3 else "?", [a, LEAF(-1), c], name="root", halo=stage == 3)


def fig_bottom_up():
    W, H = 1000, 680
    body = []
    titles = [("① Start: only the leaves are known", "pay-offs to Player 1 at the final positions"),
              ("② Nodes whose children are all known", "B1 = max(1, 2) = 2 · B2 = max(−1, 2, 1) = 2 · C = min(2, −2) = −2"),
              ("③ Next level up", "A = min(4, 2, 2) = 2"),
              ("④ The root", "root = max(2, −1, −2) = 2  →  value of the game")]
    for k in range(4):
        col, row = k % 2, k // 2
        ox, oy = 95 + col * 500, 40 + row * 300
        body.append(panel_title(ox - 70, oy, *titles[k]))
        frag, _, _ = draw_tree(l5_tree(k), unit=44, dy=68, x0=ox, y0=oy + 62,
                               level_labels=["MAX", "MIN", "MAX", ""], label_x=ox - 22, node_r=16)
        body.append(frag)
    body.append(f'<line x1="500" y1="20" x2="500" y2="{H-20}" stroke="{C["hair"]}"/>')
    body.append(f'<line x1="20" y1="320" x2="{W-20}" y2="320" stroke="{C["hair"]}"/>')
    leg, _ = legend_items(40, H - 18, [("max", "MAX node (Player 1)"), ("min", "MIN node (Player 2)"),
                                       ("leaf", "final position"), ("halo", "value just computed"), ("pv", "optimal play")])
    body.append(leg)
    save("w4-01-bottom-up.svg", "\n".join(body), W, H, "Bottom-up minimax on the Lecture 5 tree")


# ---------------------------------------------------------------------------
# Figure 2: depth-first order and memory snapshot
# ---------------------------------------------------------------------------
def fig_depth_first():
    W, H = 1000, 420
    body = []
    order = iter(range(1, 20))

    def L_(v):
        return Node("leaf", str(v))

    # post-order numbering
    l4 = L_(4); l4.badge = 1
    b1l1, b1l2 = L_(1), L_(2); b1l1.badge, b1l2.badge = 2, 3
    b1 = Node("max", "2", [b1l1, b1l2], name="B1", badge=4)
    x1, x2, x3 = L_(-1), L_(2), L_(1); x1.badge, x2.badge, x3.badge = 5, 6, 7
    b2 = Node("max", "2", [x1, x2, x3], name="B2", badge=8)
    a = Node("min", "2", [l4, b1, b2], name="A", badge=9)
    m = L_(-1); m.badge = 10
    c1, c2 = L_(2), L_(-2); c1.badge, c2.badge = 11, 12
    c = Node("min", "−2", [c1, c2], name="C", badge=13)
    root = Node("max", "2", [a, m, c], name="root", badge=14)
    body.append(panel_title(30, 28, "Order in which values become final", "badge k = the k-th value fixed (depth-first, left to right)"))
    frag, _, _ = draw_tree(root, unit=50, dy=78, x0=55, y0=110, level_labels=["MAX", "MIN", "MAX", ""], label_x=40, node_r=17)
    body.append(frag)

    # memory snapshot: algorithm is standing on leaf 2 under B2
    y1 = Node("leaf", "−1", annot2="")
    y2 = Node("leaf", "2", halo=True)
    y3 = Node("leaf", "?", faded=True)
    b2s = Node("max", "≥ −1", [y1, y2, y3], name="B2", halo=True, label_size=11)
    b1s = Node("max", "2", [Node("leaf", "1", faded=True), Node("leaf", "2", faded=True)], name="B1")
    a_s = Node("min", "≤ 2", [Node("leaf", "4", faded=True), b1s, b2s], name="A", halo=True, label_size=12)
    cs = Node("min", "?", [Node("leaf", "2", faded=True), Node("leaf", "−2", faded=True)], name="C", faded=True)
    roots = Node("max", "?", [a_s, Node("leaf", "−1", faded=True), cs], name="root", halo=True)
    body.append(f'<line x1="500" y1="20" x2="500" y2="{H-50}" stroke="{C["hair"]}"/>')
    body.append(panel_title(530, 28, "Snapshot: standing on the 5th leaf", "only the current path (highlighted) is held, plus one running value per node"))
    frag, _, _ = draw_tree(roots, unit=50, dy=78, x0=555, y0=110, level_labels=["MAX", "MIN", "MAX", ""], label_x=540, node_r=17)
    body.append(frag)
    leg, _ = legend_items(40, H - 18, [("badge", "k-th value to become final"), ("halo", "on the current path (in memory)"),
                                       ("max", "MAX"), ("min", "MIN")])
    body.append(leg)
    save("w4-02-depth-first.svg", "\n".join(body), W, H, "Depth-first minimax")


# ---------------------------------------------------------------------------
# Figure 3: the non-zero-sum game (minimax handout Exercise 1 / Figure 4)
# ---------------------------------------------------------------------------
def fig_nonzero():
    W, H = 780, 760
    body = []

    def tree(for_p1):
        P = lambda pay, **k: Node("leaf", f"({num(pay[0])}, {num(pay[1])})", **k)
        if for_p1:
            y1 = Node("max", "2", [P((1, -1)), P((2, -2), edge="pv")], name="Y1")
            y2 = Node("max", "2", [P((-1, 3)), P((2, -2), edge="pv"), P((1, 2))], name="Y2")
            x = Node("min", "2", [P((4, 3)), y1, y2], name="X", edge="pv")
            z = Node("min", "−2", [P((2, 3)), P((-2, 4))], name="Z")
            return Node("max", "2", [x, P((-1, 4)), z], name="root")
        y1 = Node("min", "−2", [P((1, -1)), P((2, -2))], name="Y1")
        y2 = Node("min", "−2", [P((-1, 3)), P((2, -2)), P((1, 2))], name="Y2")
        x = Node("max", "3", [P((4, 3), edge="pv"), y1, y2], name="X")
        z = Node("max", "4", [P((2, 3)), P((-2, 4), edge="pv")], name="Z")
        return Node("min", "3", [x, P((-1, 4)), z], name="root")

    body.append(panel_title(20, 26, "Minimax for Player 1 (first number)",
                            "P1 maximises at its own nodes, assumes P2 minimises P1's pay-off → value 2"))
    frag, _, _ = draw_tree(tree(True), unit=74, dy=80, x0=78, y0=100, level_labels=["P1: max", "P2: min", "P1: max", ""], label_x=70)
    body.append(frag)
    body.append(f'<line x1="20" y1="370" x2="{W-20}" y2="370" stroke="{C["hair"]}"/>')
    body.append(panel_title(20, 396, "Minimax for Player 2 (second number)",
                            "P2 maximises at its own nodes, assumes P1 minimises P2's pay-off → value 3"))
    frag, _, _ = draw_tree(tree(False), unit=74, dy=80, x0=78, y0=470, level_labels=["P1: min", "P2: max", "P1: min", ""], label_x=70)
    body.append(frag)
    leg, _ = legend_items(30, H - 22, [("max", "node maximising for the player analysed"), ("min", "worst-case node"),
                                       ("pv", "that player's security choices")])
    body.append(leg)
    save("w4-03-nonzero-sum.svg", "\n".join(body), W, H, "Minimax in a non-zero-sum game")


# ---------------------------------------------------------------------------
# Figure 4: why 'let the other player maximise their own pay-off' is ill-defined
# ---------------------------------------------------------------------------
def fig_tie():
    W, H = 760, 300
    body = []
    P = lambda a, b, **k: Node("leaf", f"({num(a)}, {num(b)})", **k)
    t = Node("p1", "?", [Node("p2", "?", [P(0, 3), P(5, 3)], name="P2"), P(2, 1)], name="P1")
    frag, _, _ = draw_tree(t, unit=90, dy=86, x0=40, y0=70)
    body.append(frag)
    body.append(text(30, 26, "P2 is indifferent: both moves give P2 a pay-off of 3", size=14, weight=700, anchor="start"))
    x = 330
    rows = [("Minimax for P1 (worst case)", "P2 node = min(0, 5) = 0;  root = max(0, 2) = 2", C["ink"]),
            ("‘P2 maximises its own pay-off’", "P2 node = 0 or 5?  Both moves give P2 exactly 3", C["cut"]),
            ("", "→ root = 2 or 5: no single answer, the rule is not deterministic", C["cut"])]
    yy = 96
    for a, b, col in rows:
        if a:
            body.append(text(x, yy, a, size=13, weight=700, anchor="start"))
            yy += 20
        body.append(text(x, yy, b, size=12.5, fill=col, anchor="start"))
        yy += 32
    body.append(text(x, yy + 6, "Pay-offs are written (Player 1, Player 2).", size=12, fill=C["ink2"], anchor="start", italic=True))
    save("w4-04-tie.svg", "\n".join(body), W, H, "Ties make the alternative rule non-deterministic")


# ---------------------------------------------------------------------------
# Figure 5: imperfect information
# ---------------------------------------------------------------------------
def fig_imperfect():
    W, H = 800, 360
    body = []
    t = Node("chance", "N", [
        Node("p2", "?", [Node("leaf", "−2", name="call"), Node("leaf", "−1", name="fold")], edge_label="High ½"),
        Node("p2", "?", [Node("leaf", "+2", name="call"), Node("leaf", "−1", name="fold")], edge_label="Low ½"),
    ])
    frag, _, _ = draw_tree(t, unit=95, dy=110, x0=60, y0=60)
    body.append(frag)
    # information set: dashed rounded box around the two P2 nodes at (155, 170) and (345, 170)
    body.append(f'<rect x="117" y="144" width="266" height="52" rx="26" fill="none" stroke="{C["ink2"]}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    body.append(text(250, 170, "P2", size=13, fill=C["min"], weight=700))
    body.append(text(250, 338, "dashed loop = one information set: P2 cannot tell which card P1 holds", size=11.5, fill=C["ink2"]))
    x = 470
    body.append(text(x, 40, "Pay-offs shown to P2", size=14, weight=700, anchor="start"))
    lines = [("If the card was dealt by chance:", C["ink"], 700),
             ("call = ½(−2) + ½(+2) = 0,  fold = −1  → call", C["ink2"], 400),
             ("If P1 chose which node we are at:", C["ink"], 700),
             ("call = min(−2, +2) = −2,  fold = −1  → fold", C["ink2"], 400),
             ("Real card games mix both: chance deals,", C["cut"], 700),
             ("then P1 bets knowing its card. Neither", C["cut"], 400),
             ("rule alone gives the true value.", C["cut"], 400)]
    yy = 76
    for s, col, wt in lines:
        body.append(text(x, yy, s, size=12.5, fill=col, weight=wt, anchor="start"))
        yy += 26 if wt == 700 else 30
    save("w4-05-imperfect.svg", "\n".join(body), W, H, "Imperfect information breaks plain minimax")


# ---------------------------------------------------------------------------
# Figure 6: the alpha-beta window as a number line
# ---------------------------------------------------------------------------
def fig_window():
    W, H = 900, 300
    body = []
    x0, x1 = 150, 860
    a_x, b_x = 380, 630
    grey, blue, red = "#ecebe7", "#dbe8fa", "#fbe3e3"
    for row, (title, regions) in enumerate((
            ("MAX node", [("ignore v", "move on to next child", grey),
                          ("α ← v", "raise the lower bound, next child", blue),
                          ("CUT-OFF", "MIN above will never allow this: return", red)]),
            ("MIN node", [("CUT-OFF", "MAX above will never allow this: return", red),
                          ("β ← v", "lower the upper bound, next child", blue),
                          ("ignore v", "move on to next child", grey)]))):
        y = 70 + row * 110
        body.append(text(x0 - 18, y + 22, title, size=14, weight=700, anchor="end",
                         fill=C["max"] if row == 0 else C["min"]))
        spans = [(x0, a_x), (a_x, b_x), (b_x, x1)]
        for (sx, ex), (h, s, col) in zip(spans, regions):
            body.append(f'<rect x="{sx+1}" y="{y}" width="{ex-sx-2}" height="44" rx="6" fill="{col}"/>')
            body.append(text((sx + ex) / 2, y + 15, h, size=14, weight=700,
                             fill=C["cut"] if h == "CUT-OFF" else C["ink"]))
            body.append(text((sx + ex) / 2, y + 32, s, size=11.5, fill=C["ink2"]))
        for xx, lab in ((a_x, "α"), (b_x, "β")):
            body.append(f'<line x1="{xx}" y1="{y-8}" x2="{xx}" y2="{y+52}" stroke="{C["ink"]}" stroke-width="2"/>')
            body.append(text(xx, y - 18, lab, size=15, weight=700))
        body.append(text((x0 + a_x) / 2, y + 62, "v ≤ α", size=12.5, family="'DejaVu Sans Mono', monospace", fill=C["ink2"]))
        body.append(text((a_x + b_x) / 2, y + 62, "α < v < β", size=12.5, family="'DejaVu Sans Mono', monospace", fill=C["ink2"]))
        body.append(text((b_x + x1) / 2, y + 62, "v ≥ β", size=12.5, family="'DejaVu Sans Mono', monospace", fill=C["ink2"]))
    body.append(text(x0, 28, "Where does the value v just returned by a child fall, relative to the window (α, β)?",
                     size=14, weight=700, anchor="start"))
    save("w4-06-window.svg", "\n".join(body), W, H, "The alpha-beta update rules")


# ---------------------------------------------------------------------------
# Figure 7: Lecture 6 handout example (Figures 1-9), final state
# ---------------------------------------------------------------------------
def fig_l6_example():
    W, H = 900, 580
    body = []
    T = lambda lab="": Node("tri", lab)
    c = Node("min", "≤−4", [Node("leaf", "−4"), T()], name="C", annot="[−2, 4]", label_size=11)
    c.children[1].edge = "pruned"
    b = Node("max", "−2", [Node("leaf", "−2"), c], name="B", annot="(−∞, 4]")
    d = Node("max", "≥1", [Node("leaf", "1"), T(), T()], name="D", annot="(−∞, −2]", label_size=12)
    d.children[1].edge = d.children[2].edge = "pruned"
    a = Node("min", "−2", [Node("leaf", "4"), b, d], name="A", annot="(−∞, ∞)")
    e = Node("min", "≤−1", [Node("leaf", "−1"), T()], name="E", annot="[1, ∞)", label_size=11)
    e.children[1].edge = "pruned"
    mid = Node("leaf", "1", name="(a subtree worth 1)")
    a.edge = "normal"
    mid.edge = "pv"
    root = Node("max", "1", [a, mid, e], name="root", annot="(−∞, ∞)")
    frag, _, _ = draw_tree(root, unit=72, dy=92, x0=110, y0=80, level_labels=["MAX", "MIN", "MAX", "MIN"], label_x=70)
    body.append(frag)
    body.append(text(30, 30, "Lecture 6 example: the window each node was entered with, and what was learnt",
                     size=14, weight=700, anchor="start"))
    notes = ["① C: −4 ≤ α = −2 → C cannot matter to B",
             "② D: 1 ≥ β = −2 → D cannot matter to A",
             "③ E: −1 ≤ α = 1 → E cannot matter to the root"]
    for i, s in enumerate(notes):
        body.append(text(560, 452 + i * 26, s, size=12.5, anchor="start", fill=C["ink2"]))
    leg, _ = legend_items(30, H - 20, [("pruned", "pruned edge"), ("tri", "subtree never visited"),
                                       ("max", "MAX"), ("min", "MIN")])
    body.append(leg)
    body.append(text(560, 424, "[α, β] next to a node = window passed down to it", size=12, anchor="start", fill=C["ink2"], italic=True))
    save("w4-07-ab-lecture6.svg", "\n".join(body), W, H, "Alpha-beta: Lecture 6 example")


# ---------------------------------------------------------------------------
# Figure 8: alpha-beta on the Lecture 5 tree
# ---------------------------------------------------------------------------
def fig_ab_l5():
    W, H = 760, 380
    body = []
    b1 = Node("max", "2", [LEAF(1), LEAF(2)], name="B1", annot="(−∞, 4]")
    b2 = Node("max", "≥2", [LEAF(-1), LEAF(2), LEAF(1, edge="pruned")], name="B2", annot="(−∞, 2]", label_size=12)
    a = Node("min", "2", [LEAF(4), b1, b2], name="A", annot="(−∞, ∞)")
    c = Node("min", "≤2", [LEAF(2), LEAF(-2, edge="pruned")], name="C", annot="[2, ∞)", label_size=12)
    root = Node("max", "2", [a, LEAF(-1), c], name="root", annot="(−∞, ∞)")
    frag, _, _ = draw_tree(root, unit=62, dy=88, x0=90, y0=80, level_labels=["MAX", "MIN", "MAX", ""], label_x=64)
    body.append(frag)
    body.append(text(30, 30, "The Lecture 5 tree again, now with alpha-beta: 7 of 9 leaves are read", size=14, weight=700, anchor="start"))
    leg, _ = legend_items(30, H - 20, [("pruned", "pruned (never read)"), ("max", "MAX"), ("min", "MIN")])
    body.append(leg)
    save("w4-08-ab-lecture5-tree.svg", "\n".join(body), W, H, "Alpha-beta on the Lecture 5 tree")


# ---------------------------------------------------------------------------
# Figures 9, 10: Lecture 7 worked examples
# ---------------------------------------------------------------------------
def fig_l7_ex1():
    W, H = 820, 470
    body = []
    n31 = Node("min", "−3", [LEAF(-3)], name="3.1", edge="pruned")
    n21 = Node("max", "≥3", [LEAF(3), n31], name="2.1", annot="(−∞, 2]", label_size=12)
    c1 = Node("min", "2", [LEAF(2), n21], name="C1", annot="(−∞, ∞)")
    n22 = Node("max", "3", [LEAF(3)], name="2.2", edge="pruned")
    c2 = Node("min", "≤−3", [LEAF(-3), n22], name="C2", annot="[2, ∞)", label_size=11)
    n23 = Node("max", "≥4", [LEAF(4)], name="2.3", annot="[2, 3]", label_size=12)
    c3 = Node("min", "3", [LEAF(3), n23], name="C3", annot="[2, ∞)", edge="pv")
    root = Node("max", "3", [c1, c2, c3], name="Root", annot="(−∞, ∞)")
    frag, _, _ = draw_tree(root, unit=84, dy=88, x0=90, y0=80, level_labels=["MAX", "MIN", "MAX", "MIN", ""], label_x=64)
    body.append(frag)
    body.append(text(30, 30, "Lecture 7, worked example 1: value 3, best move C3, 5 of 7 leaves read", size=14, weight=700, anchor="start"))
    leg, _ = legend_items(30, H - 20, [("pruned", "pruned (faded values are never computed)"), ("pv", "best move"),
                                       ("max", "MAX"), ("min", "MIN")])
    body.append(leg)
    save("w4-09-ab-l7-example1.svg", "\n".join(body), W, H, "Alpha-beta: Lecture 7 example 1")


def fig_l7_ex2():
    W, H = 980, 560
    body = []
    n41 = Node("max", "10", [LEAF(-13), LEAF(10)], name="4.1")
    n42 = Node("max", "12", [LEAF(12), LEAF(-12)], name="4.2")
    n31 = Node("min", "10", [n41, n42], name="3.1", edge="pruned")
    n21 = Node("max", "≥4", [LEAF(4), n31], name="2.1", annot="(−∞, −3]", label_size=12)
    c1 = Node("min", "−3", [LEAF(-3), n21], name="C1", annot="(−∞, ∞)")
    n32 = Node("min", "≤−13", [LEAF(-13), LEAF(-10, edge="pruned")], name="3.2", annot="[−3, ∞)", label_size=10)
    n22 = Node("max", "≤−3", [n32], name="2.2", annot="[−3, ∞)", label_size=10)
    c2 = Node("min", "≤−3", [n22], name="C2", annot="[−3, ∞)", label_size=10)
    n43 = Node("max", "−3", [LEAF(-4), LEAF(-3)], name="4.3")
    n44 = Node("max", "6", [LEAF(6), LEAF(5)], name="4.4")
    n33 = Node("min", "−3", [n43, n44], name="3.3", edge="pruned")
    n23 = Node("max", "≥5", [LEAF(5), n33], name="2.3", annot="[−3, 4]", label_size=12)
    c3 = Node("min", "4", [LEAF(4), n23], name="C3", annot="[−3, ∞)", edge="pv")
    root = Node("max", "4", [c1, c2, c3], name="Root", annot="(−∞, ∞)")
    frag, _, _ = draw_tree(root, unit=64, dy=88, x0=70, y0=80, level_labels=["MAX", "MIN", "MAX", "MIN", "MAX", ""], label_x=52)
    body.append(frag)
    body.append(text(30, 30, "Lecture 7, worked example 2: value 4, best move C3, only 5 of 14 leaves read", size=14, weight=700, anchor="start"))
    leg, _ = legend_items(30, H - 20, [("pruned", "pruned (faded values are never computed)"), ("pv", "best move"),
                                       ("max", "MAX"), ("min", "MIN")])
    body.append(leg)
    save("w4-10-ab-l7-example2.svg", "\n".join(body), W, H, "Alpha-beta: Lecture 7 example 2")


# ---------------------------------------------------------------------------
# Figure 11: depth-limited search with an evaluation function
# ---------------------------------------------------------------------------
def fig_depth_limited():
    W, H = 900, 440
    body = []
    T = lambda: Node("tri", "", faded=True)

    def F(v):  # frontier node with evaluation
        n = Node("leaf", v)
        n.children = []
        return n

    m1 = Node("min", "−0.4", [F("e = 0.3"), F("e = −0.4"), F("e = 0.2")], name="")
    m2 = Node("min", "+1", [Node("leaf", "U = +1", name="terminal: a win")], name="")
    m3 = Node("min", "0.1", [F("e = 0.1"), F("e = 0.6")], name="")
    m2.edge = "pv"
    root = Node("max", "+1", [m1, m2, m3], name="root")
    frag, _, _ = draw_tree(root, unit=100, dy=110, x0=130, y0=70, level_labels=["MAX", "MIN", "depth 2"], label_x=90)
    body.append(frag)
    yline = 70 + 2 * 110 + 30
    body.append(f'<line x1="40" y1="{yline}" x2="{W-40}" y2="{yline}" stroke="{C["cut"]}" stroke-width="1.6" stroke-dasharray="8 5"/>')
    body.append(text(W - 40, yline + 16, "depth limit d = 2: nothing below this line is generated", size=12.5, fill=C["cut"], anchor="end", weight=600))
    for xx in (180, 280, 380, 580, 680):
        body.append(f'<polygon points="{xx},{yline+12} {xx+26},{yline+64} {xx-26},{yline+64}" fill="#fafaf8" stroke="{C["hair"]}" stroke-dasharray="4 3"/>')
    body.append(text(430, yline + 92, "the rest of the game, too big to search: the evaluation function e(J) stands in for it",
                     size=12.5, fill=C["ink2"]))
    body.append(text(30, 28, "Depth-limited minimax: true pay-offs U(J) where the game ends, guesses e(J) in (−1, 1) at the frontier",
                     size=14, weight=700, anchor="start"))
    save("w4-11-depth-limited.svg", "\n".join(body), W, H, "Depth-limited search")


# ---------------------------------------------------------------------------
# Figure 12: tic-tac-toe depth-2 search (redrawn and corrected)
# ---------------------------------------------------------------------------
def fig_ttt_depth2():
    W, H = 1010, 520
    s0, s1, s2 = 56, 50, 44
    body = []
    root = (W / 2 + 30, 70)
    groups = [("X........", [("X..O.....", "6−5 = 1"), ("X.....O..", "5−5 = 0"), ("X......O.", "6−5 = 1"),
                             ("X.......O", "5−5 = 0*"), ("X...O....", "4−5 = −1")], "−1"),
              ("...X.....", [("O..X.....", "5−6 = −1"), (".O.X.....", "6−6 = 0*"), ("..OX.....", "5−6 = −1"),
                             ("...X.O...", "6−6 = 0"), ("...XO....", "4−6 = −2")], "−2"),
              ("....X....", [("O...X....", "5−4 = 1"), ("...OX....", "6−4 = 2")], "1")]
    xs_mid = [200, 560, 860]
    leaf_x = []
    lx = 104
    for gi, (_, kids, _) in enumerate(groups):
        for _ in kids:
            leaf_x.append(lx)
            lx += 64
        lx += 40
    body.append(board(root[0] - s0 / 2, root[1] - s0 / 2, s0, "........."))
    body.append(text(root[0] + 44, root[1] - 8, "MAX (X)", size=12, fill=C["max"], weight=700, anchor="start"))
    body.append(text(root[0] + 44, root[1] + 10, "value 1 → play the centre", size=12.5, weight=700, anchor="start"))
    k = 0
    for gi, (cells, kids, mval) in enumerate(groups):
        n = len(kids)
        first = leaf_x[k] + s2 / 2
        last = leaf_x[k + n - 1] + s2 / 2
        mx, my = (first + last) / 2, 210
        best = gi == 2
        body.append(f'<line x1="{root[0]}" y1="{root[1]+s0/2}" x2="{mx}" y2="{my-s1/2-2}" stroke="{C["pv"] if best else C["edge"]}" stroke-width="{3 if best else 1.6}"/>')
        body.append(board(mx - s1 / 2, my - s1 / 2, s1, cells))
        body.append(f'<rect x="{mx+s1/2+6}" y="{my-12}" width="{30+8*len(mval)}" height="24" rx="12" fill="{C["min_fill"]}" stroke="{C["min"]}"/>')
        body.append(text(mx + s1 / 2 + 21 + 4 * len(mval), my, mval, size=13, weight=700))
        for j, (c2, lab) in enumerate(kids):
            bx = leaf_x[k]
            by = 360
            body.append(f'<line x1="{mx}" y1="{my+s1/2}" x2="{bx+s2/2}" y2="{by-2}" stroke="{C["edge"]}" stroke-width="1.3"/>')
            body.append(board(bx, by, s2, c2))
            star = lab.endswith("*")
            body.append(text(bx + s2 / 2, by + s2 + 16, lab.rstrip("*"), size=12, weight=700,
                             fill=C["cut"] if star else C["ink"], family="'DejaVu Sans Mono', monospace"))
            if star:
                body.append(text(bx + s2 / 2, by + s2 + 33, "slide: " + ("5−5 = 1" if gi == 0 else "5−5 = 0"),
                                 size=10.5, fill=C["cut"]))
            k += 1
    body.append(text(30, 210, "MIN (O)", size=12, fill=C["min"], weight=700, anchor="start"))
    body.append(text(30, 382, "depth 2:", size=12, fill=C["ink2"], weight=700, anchor="start"))
    body.append(text(30, 398, "evaluate", size=12, fill=C["ink2"], anchor="start"))
    body.append(text(30, 470, "h = (lines still open for X) − (lines still open for O), evaluated for X; "
                              "one representative of each symmetric reply shown.", size=12.5, fill=C["ink2"], anchor="start"))
    body.append(text(30, 492, "Red labels: corrected arithmetic (the slide prints 5−5 = 1 under the corner node, and 5−5 = 0 where it should be 6−6 = 0).",
                     size=12.5, fill=C["cut"], anchor="start"))
    body.append(text(30, 30, "Tic-tac-toe searched to depth 2 with the open-lines heuristic", size=14, weight=700, anchor="start"))
    save("w4-12-ttt-depth2.svg", "\n".join(body), W, H, "Tic-tac-toe depth-2 search")


# ---------------------------------------------------------------------------
# Figure 13: the eight lines + the slide-14 position sequence
# ---------------------------------------------------------------------------
def fig_ttt_lines():
    W, H = 980, 330
    body = []
    s = 150
    x, y = 70, 80
    body.append(board(x, y, s, "........."))
    cols = ["#2a78d6", "#eb6834", "#1baf7a", "#6250d6"]
    c = s / 3
    segs = []
    for r in range(3):
        segs.append(((x + 10, y + c * r + c / 2), (x + s - 10, y + c * r + c / 2), cols[0]))
        segs.append(((x + c * r + c / 2, y + 10), (x + c * r + c / 2, y + s - 10), cols[1]))
    segs.append(((x + 12, y + 12), (x + s - 12, y + s - 12), cols[2]))
    segs.append(((x + s - 12, y + 12), (x + 12, y + s - 12), cols[3]))
    for (a, b, col) in segs:
        body.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{col}" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    body.append(text(x + s / 2, y + s + 20, "8 lines: 3 rows,", size=12.5, fill=C["ink2"]))
    body.append(text(x + s / 2, y + s + 38, "3 columns, 2 diagonals", size=12.5, fill=C["ink2"]))
    body.append(text(40, 40, "Where can anyone still win?", size=14, weight=700, anchor="start"))
    seq = [("..X.XO...", "O to move", "6 − 2 = 4", [2, 4, 6]),
           ("..X.XOO..", "X to move", "3 − 2 = 1", None),
           ("X.X.XOO..", "O to move", "3 − 1 = 2", [1, 8])]
    bx = 300
    body.append(text(bx, 40, "The slide-14 sequence, scored for X", size=14, weight=700, anchor="start"))
    for i, (cells, who, val, hl) in enumerate(seq):
        xx = bx + i * 225
        body.append(board(xx, y, 120, cells, hl=hl, hl_color="#fde7c7" if i == 0 else "#fbe3e3"))
        body.append(text(xx + 60, y + 140, who, size=12, fill=C["ink2"]))
        body.append(text(xx + 60, y + 162, "h = " + val, size=13, weight=700, family="'DejaVu Sans Mono', monospace"))
        body.append(text(xx + 60, y + 184, "true value: X wins (+1)", size=12, fill=C["ink2"]))
        if i < 2:
            body.append(f'<path d="M{xx+132},{y+60} L{xx+208},{y+60}" stroke="{C["muted"]}" stroke-width="1.6" marker-end="url(#arr)"/>')
    body.append(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C["muted"]}"/></marker></defs>')
    body.append(text(bx, y + 222, "① X threatens the shaded diagonal, so O must block.   ③ X has a fork (two shaded squares); O can block only one.",
                     size=12, fill=C["ink2"], anchor="start"))
    save("w4-13-ttt-lines.svg", "\n".join(body), W, H, "The open-lines heuristic")


# ---------------------------------------------------------------------------
# Figure 14: Othello position from the slides
# ---------------------------------------------------------------------------
def fig_othello():
    rows = ["....W...", "....W...", "W.BWWB..", "WWBBWB..", "WWWWWB..", "..BWBB..", "...BWB..", "BBBBBB.."]
    black_moves = ["d1", "f1", "c2", "d2", "f2", "a6", "b6", "c7"]
    white_moves = ["b2", "c2", "d2", "g2", "b3", "g3", "g4", "g5", "b6", "g6", "b7", "c7", "g7", "g8"]
    stable = ["a8", "b8", "c8", "d8", "e8", "f8"]
    W, H = 960, 470
    body = []

    def sq(name):
        return "abcdefgh".index(name[0]), int(name[1]) - 1

    def draw(ox, oy, moves, mark_stable, title, sub):
        cs = 40
        body.append(text(ox, oy - 40, title, size=14, weight=700, anchor="start"))
        body.append(text(ox, oy - 20, sub, size=12, fill=C["ink2"], anchor="start"))
        body.append(f'<rect x="{ox}" y="{oy}" width="{8*cs}" height="{8*cs}" fill="#3f8f5f" rx="3"/>')
        for i in range(9):
            body.append(f'<line x1="{ox+i*cs}" y1="{oy}" x2="{ox+i*cs}" y2="{oy+8*cs}" stroke="#2c6b45" stroke-width="1"/>')
            body.append(f'<line x1="{ox}" y1="{oy+i*cs}" x2="{ox+8*cs}" y2="{oy+i*cs}" stroke="#2c6b45" stroke-width="1"/>')
        for q in range(8):
            body.append(text(ox + q * cs + cs / 2, oy + 8 * cs + 12, "abcdefgh"[q], size=11, fill=C["ink2"]))
            body.append(text(ox - 10, oy + q * cs + cs / 2, str(q + 1), size=11, fill=C["ink2"]))
        for (cx, cy) in ((0, 0), (7, 0), (0, 7), (7, 7)):
            body.append(f'<rect x="{ox+cx*cs+2}" y="{oy+cy*cs+2}" width="{cs-4}" height="{cs-4}" fill="none" stroke="#f4d35e" stroke-width="2.5" rx="3"/>')
        for r, row in enumerate(rows):
            for q, ch in enumerate(row):
                if ch in "BW":
                    fill = "#111111" if ch == "B" else "#fafafa"
                    body.append(f'<circle cx="{ox+q*cs+cs/2}" cy="{oy+r*cs+cs/2}" r="{cs*0.4}" fill="{fill}" stroke="#1d4d31" stroke-width="1"/>')
        if mark_stable:
            for nme in stable:
                q, r = sq(nme)
                body.append(text(ox + q * cs + cs / 2, oy + r * cs + cs / 2 + 0.5, "★", size=14, fill="#f4d35e"))
        for nme in moves:
            q, r = sq(nme)
            body.append(f'<circle cx="{ox+q*cs+cs/2}" cy="{oy+r*cs+cs/2}" r="7" fill="none" stroke="#ffffff" stroke-width="2.2"/>')

    draw(40, 90, black_moves, True, "If Black moves: 8 legal moves", "rings = legal moves · ★ = stable black discs · yellow squares = corners")
    draw(520, 90, white_moves, False, "If White moves: 14 legal moves", "rings = legal moves")
    save("w4-14-othello.svg", "\n".join(body), W, H, "Othello position from the slides")


# ---------------------------------------------------------------------------
# Figure 15: Connect-4 lines
# ---------------------------------------------------------------------------
def fig_connect4():
    W, H = 900, 380
    body = []
    cs = 40
    ox, oy = 40, 70
    body.append(f'<rect x="{ox-6}" y="{oy-6}" width="{7*cs+12}" height="{6*cs+12}" rx="10" fill="#2a5db0"/>')
    for r in range(6):
        for q in range(7):
            body.append(f'<circle cx="{ox+q*cs+cs/2}" cy="{oy+r*cs+cs/2}" r="15" fill="#ffffff"/>')
    examples = [((5, 0), (0, 1), "#eb6834", "horizontal: 6 rows × 4 = 24"),
                ((2, 6), (1, 0), "#1baf7a", "vertical: 7 columns × 3 = 21"),
                ((2, 1), (1, 1), "#eda100", "diagonal ↘: 3 × 4 = 12"),
                ((5, 2), (-1, 1), "#e87ba4", "diagonal ↗: 3 × 4 = 12")]
    for (r, q), (dr, dq), col, _ in examples:
        x1, y1 = ox + q * cs + cs / 2, oy + r * cs + cs / 2
        x2, y2 = ox + (q + 3 * dq) * cs + cs / 2, oy + (r + 3 * dr) * cs + cs / 2
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="16" stroke-linecap="round" opacity="0.85"/>')
    body.append(text(ox, 36, "Every possible four-in-a-row on a 7 × 6 board", size=14, weight=700, anchor="start"))
    tx = 400
    for i, (_, _, col, lab) in enumerate(examples):
        y = 100 + i * 40
        body.append(f'<line x1="{tx}" y1="{y}" x2="{tx+30}" y2="{y}" stroke="{col}" stroke-width="10" stroke-linecap="round"/>')
        body.append(text(tx + 44, y, lab, size=13, anchor="start"))
    body.append(f'<line x1="{tx}" y1="262" x2="{tx+430}" y2="262" stroke="{C["hair"]}"/>')
    body.append(text(tx, 286, "Total: 69 possible winning lines", size=14, weight=700, anchor="start"))
    body.append(text(tx, 312, "A line is unblocked for a player if the opponent has no disc in it.", size=12.5, fill=C["ink2"], anchor="start"))
    body.append(text(tx, 334, "h = (unblocked lines for P1) − (unblocked lines for P2)", size=12.5, fill=C["ink2"], anchor="start"))
    save("w4-15-connect4.svg", "\n".join(body), W, H, "Connect-4 lines")


# ---------------------------------------------------------------------------
# Figure 16: Chomp and Nim (alpha-beta handout exercise)
# ---------------------------------------------------------------------------
def fig_chomp_nim():
    W, H = 980, 470
    body = []
    cs = 44

    def bar(ox, oy, rows_len, label, sub="", taken=None, cross=None):
        # rows_len = (bottom, top); draw 2 rows x 3 cols, bottom row at bottom
        for r in range(2):
            for q in range(3):
                x, y = ox + q * cs, oy + (1 - r) * cs
                present = q < rows_len[r]
                if present:
                    fill = "#8a5a3c" if not (r == 0 and q == 0) else "#c0392b"
                    body.append(f'<rect x="{x+1}" y="{y+1}" width="{cs-2}" height="{cs-2}" rx="5" fill="{fill}"/>')
                    if r == 0 and q == 0:
                        body.append(text(x + cs / 2, y + cs / 2 + 1, "P", size=19, fill="#ffffff", weight=800))
                else:
                    body.append(f'<rect x="{x+1}" y="{y+1}" width="{cs-2}" height="{cs-2}" rx="5" fill="none" stroke="{C["hair"]}" stroke-dasharray="4 3"/>')
                if cross == (r, q):
                    body.append(f'<rect x="{x+1}" y="{y+1}" width="{cs-2}" height="{cs-2}" rx="5" fill="none" stroke="#eda100" stroke-width="3"/>')
        body.append(text(ox + 1.5 * cs, oy + 2 * cs + 18, label, size=12.5, weight=700))
        if sub:
            body.append(text(ox + 1.5 * cs, oy + 2 * cs + 36, sub, size=11.5, fill=C["ink2"]))

    body.append(text(30, 30, "2 × 3 Chomp: whoever eats the poisoned square (P, bottom-left) loses", size=14, weight=700, anchor="start"))
    bar(40, 70, (3, 3), "start", "P1 to move", cross=(1, 2))
    body.append(f'<path d="M190,114 L240,114" stroke="{C["muted"]}" stroke-width="1.6" marker-end="url(#a2)"/>')
    bar(260, 70, (3, 2), "after P1 eats top-right", "P2 to move: LOSING")
    body.append(text(470, 92, "Positions where the player to move loses:", size=12.5, weight=700, anchor="start"))
    bar(480, 120, (3, 2), "3 / 2")
    bar(640, 120, (2, 1), "2 / 1")
    bar(800, 120, (1, 0), "1 / 0", "only poison left")
    for i, ln in enumerate(["Pattern: the bottom row is exactly one square longer than the top row.",
                            "Every move from such a position breaks the pattern, the opponent can",
                            "always restore it, and in the end the mover faces the poison alone."]):
        body.append(text(470, 262 + i * 18, ln, size=12, fill=C["ink2"], anchor="start"))
    body.append(f'<line x1="20" y1="320" x2="{W-20}" y2="320" stroke="{C["hair"]}"/>')
    body.append(text(30, 346, "(3, 3, 3)-Nim: take any number from one heap", size=14, weight=700, anchor="start"))

    def heaps(ox, oy, hs, lab):
        for i, h in enumerate(hs):
            for j in range(3):
                x = ox + i * 46
                y = oy + (2 - j) * 22
                if j < h:
                    body.append(f'<rect x="{x}" y="{y}" width="34" height="16" rx="4" fill="#2a78d6"/>')
                else:
                    body.append(f'<rect x="{x}" y="{y}" width="34" height="16" rx="4" fill="none" stroke="{C["hair"]}" stroke-dasharray="4 3"/>')
        body.append(text(ox + 57, oy + 82, lab, size=12.5, weight=700))

    heaps(40, 370, (3, 3, 3), "(3, 3, 3): P1 to move")
    body.append(f'<path d="M190,405 L240,405" stroke="{C["muted"]}" stroke-width="1.6" marker-end="url(#a2)"/>')
    heaps(260, 370, (3, 3, 0), "(3, 3, 0): P2 to move")
    body.append(text(430, 386, "Winning move: empty one heap. Two equal heaps remain, so P1 copies", size=12, fill=C["ink2"], anchor="start"))
    body.append(text(430, 404, "every move of P2 on the other heap (the mirror strategy). P1 always has", size=12, fill=C["ink2"], anchor="start"))
    body.append(text(430, 422, "a reply, so P1 takes the last stick. (Same first move wins if taking", size=12, fill=C["ink2"], anchor="start"))
    body.append(text(430, 440, "the last stick loses; only the very end of the play changes.)", size=12, fill=C["ink2"], anchor="start"))
    body.append(f'<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C["muted"]}"/></marker></defs>')
    save("w4-16-chomp-nim.svg", "\n".join(body), W, H, "Chomp and Nim")


if __name__ == "__main__":
    fig_bottom_up()
    fig_depth_first()
    fig_nonzero()
    fig_tie()
    fig_imperfect()
    fig_window()
    fig_l6_example()
    fig_ab_l5()
    fig_l7_ex1()
    fig_l7_ex2()
    fig_depth_limited()
    fig_ttt_depth2()
    fig_ttt_lines()
    fig_othello()
    fig_connect4()
    fig_chomp_nim()
    print("done")
