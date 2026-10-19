"""Tiny SVG toolkit for the Week 4 figures: game trees, mini boards, captions."""
from html import escape

FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'DejaVu Sans Mono', Menlo, Consolas, monospace"

C = {
    "bg": "#ffffff",
    "ink": "#0b0b0b",
    "ink2": "#52514e",
    "muted": "#8a8984",
    "hair": "#d9d8d3",
    "edge": "#a9a8a2",
    "max": "#2a78d6",
    "max_fill": "#eef4fc",
    "min": "#eb6834",
    "min_fill": "#fdf0ea",
    "chance": "#1baf7a",
    "chance_fill": "#e9f7f1",
    "leaf_fill": "#f3f3f1",
    "pv": "#0b0b0b",
    "cut": "#e34948",
    "halo": "#eda100",
    "new": "#fff4d6",
}


def num(v):
    """Typographic number: real minus sign, infinity symbol."""
    if isinstance(v, str):
        return v.replace("-inf", "−∞").replace("+inf", "+∞").replace("inf", "∞").replace("-", "−")
    if v == float("inf"):
        return "∞"
    if v == float("-inf"):
        return "−∞"
    s = str(v)
    return s.replace("-", "−")


def text(x, y, s, size=14, weight=400, fill=None, anchor="middle", family=FONT, italic=False, extra=""):
    fill = fill or C["ink"]
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="central"{st} {extra}>{escape(s)}</text>')


class Node:
    def __init__(self, kind, label="", children=None, name="", edge="normal", annot="", annot2="",
                 badge=None, halo=False, faded=False, edge_label="", width=1.0, label_size=None):
        self.kind = kind            # max | min | leaf | chance | tri (unexplored subtree) | p1 | p2
        self.label = label
        self.children = children or []
        self.name = name
        self.edge = edge            # normal | pv | pruned | dim
        self.annot = annot          # text right of node (e.g. window)
        self.annot2 = annot2        # text below node
        self.badge = badge          # small numbered circle
        self.halo = halo
        self.faded = faded
        self.edge_label = edge_label
        self.width = width
        self.label_size = label_size


def layout(root, unit, dy, x0, y0):
    pos = {}
    cursor = [x0]

    def rec(n, depth):
        if not n.children:
            w = unit * n.width
            x = cursor[0] + w / 2
            cursor[0] += w
        else:
            for c in n.children:
                rec(c, depth + 1)
            x = (pos[id(n.children[0])][0] + pos[id(n.children[-1])][0]) / 2
        pos[id(n)] = (x, y0 + depth * dy)

    rec(root, 0)
    return pos, cursor[0]


def mark_faded(n, faded=False):
    if n.edge == "pruned":
        faded = True
    n.faded = n.faded or faded
    for c in n.children:
        mark_faded(c, n.faded)


def draw_tree(root, unit=70, dy=86, x0=0, y0=0, level_labels=None, label_x=None, node_r=19, scissors=True):
    """Return (svg_fragment, width_used, height_used)."""
    mark_faded(root)
    pos, xend = layout(root, unit, dy, x0, y0)
    out = []
    edges, nodes, over = [], [], []

    def rec(n, depth):
        x, y = pos[id(n)]
        for c in n.children:
            cx, cy = pos[id(c)]
            r1 = node_r if n.kind != "leaf" else 12
            r2 = node_r if c.kind not in ("leaf", "tri") else 13
            if c.kind == "tri":
                r2 = 2
            # shorten edges so they meet node outlines
            import math
            dx, dyy = cx - x, cy - y
            L = math.hypot(dx, dyy)
            ux, uy = dx / L, dyy / L
            sx, sy = x + ux * r1, y + uy * r1
            ex, ey = cx - ux * r2, cy - uy * r2
            if c.edge == "pv" and not c.faded:
                edges.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{C["pv"]}" stroke-width="3.2" stroke-linecap="round"/>')
            elif c.edge == "pruned":
                edges.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{C["cut"]}" stroke-width="1.6" stroke-dasharray="5 4" stroke-linecap="round" opacity="0.85"/>')
                if scissors:
                    mx, my = (sx + ex) / 2, (sy + ey) / 2
                    over.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="8.5" fill="#ffffff" stroke="{C["cut"]}" stroke-width="1.4"/>')
                    over.append(f'<path d="M{mx-3.6:.1f},{my-3.6:.1f} L{mx+3.6:.1f},{my+3.6:.1f} M{mx+3.6:.1f},{my-3.6:.1f} L{mx-3.6:.1f},{my+3.6:.1f}" '
                                f'stroke="{C["cut"]}" stroke-width="2" stroke-linecap="round"/>')
            elif c.faded or c.edge == "dim":
                edges.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{C["hair"]}" stroke-width="1.4" stroke-dasharray="5 4"/>')
            else:
                edges.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{C["edge"]}" stroke-width="1.6" stroke-linecap="round"/>')
            if c.edge_label:
                mx, my = (sx + ex) / 2, (sy + ey) / 2
                bw = 7.2 * len(c.edge_label) + 10
                over.append(f'<rect x="{mx-bw/2:.1f}" y="{my-9:.1f}" width="{bw:.1f}" height="18" rx="4" fill="#ffffff"/>')
                over.append(text(mx, my, c.edge_label, size=12, fill=C["ink2"], italic=True))
            rec(c, depth + 1)
        op = ' opacity="0.38"' if n.faded else ""
        g = [f"<g{op}>"]
        if n.halo:
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r+9}" fill="{C["new"]}" stroke="{C["halo"]}" stroke-width="2"/>')
        ls = n.label_size or (15 if len(n.label) <= 3 else 13)
        if n.kind == "max":
            s = node_r * 2 - 2
            g.append(f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s}" height="{s}" rx="5" fill="{C["max_fill"]}" stroke="{C["max"]}" stroke-width="2"/>')
            g.append(text(x, y, num(n.label), size=ls, weight=700))
        elif n.kind == "min":
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" fill="{C["min_fill"]}" stroke="{C["min"]}" stroke-width="2"/>')
            g.append(text(x, y, num(n.label), size=ls, weight=700))
        elif n.kind == "chance":
            s = node_r * 1.25
            g.append(f'<polygon points="{x},{y-s} {x+s},{y} {x},{y+s} {x-s},{y}" fill="{C["chance_fill"]}" stroke="{C["chance"]}" stroke-width="2"/>')
            g.append(text(x, y, num(n.label), size=ls - 1, weight=700))
        elif n.kind in ("p1", "p2"):
            col, fill = (C["max"], C["max_fill"]) if n.kind == "p1" else (C["min"], C["min_fill"])
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" fill="{fill}" stroke="{col}" stroke-width="2"/>')
            g.append(text(x, y, num(n.label), size=ls, weight=700))
        elif n.kind == "tri":
            g.append(f'<polygon points="{x},{y} {x+22},{y+38} {x-22},{y+38}" fill="#fafaf8" stroke="{C["muted"]}" stroke-width="1.3" stroke-dasharray="4 3"/>')
            g.append(text(x, y + 26, n.label or "…", size=12, fill=C["ink2"], weight=600))
        else:  # leaf
            w = max(28, 8.4 * len(num(n.label)) + 12)
            g.append(f'<rect x="{x-w/2:.1f}" y="{y-12:.1f}" width="{w:.1f}" height="24" rx="5" fill="{C["leaf_fill"]}"/>')
            g.append(text(x, y, num(n.label), size=ls, weight=600))
        if n.name:
            if n.kind in ("leaf",):
                g.append(text(x, y + 22, n.name, size=11, fill=C["muted"]))
            else:
                off = node_r + (14 if n.halo else 6)
                g.append(text(x - off, y - node_r + 2, n.name, size=12, fill="#ffffff", anchor="end", weight=600,
                              extra='stroke="#ffffff" stroke-width="4" stroke-linejoin="round"'))
                g.append(text(x - off, y - node_r + 2, n.name, size=12, fill=C["ink2"], anchor="end", weight=600))
        if n.annot:
            ax = x + node_r + 7
            g.append(text(ax, y, num(n.annot), size=12, fill=C["ink2"], anchor="start", family=MONO))
        if n.annot2:
            g.append(text(x, y + node_r + 13, num(n.annot2), size=12, fill=C["ink2"], family=MONO))
        if n.badge is not None:
            bx, by = x + node_r - 2, y - node_r + 2
            g.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9.5" fill="{C["ink"]}"/>')
            g.append(text(bx, by + 0.5, str(n.badge), size=11, fill="#ffffff", weight=700))
        g.append("</g>")
        nodes.append("".join(g))

    rec(root, 0)
    depth = 0

    def maxdepth(n, d):
        nonlocal depth
        depth = max(depth, d)
        for c in n.children:
            maxdepth(c, d + 1)

    maxdepth(root, 0)
    if level_labels:
        lx = label_x if label_x is not None else x0 - 10
        for i, lab in enumerate(level_labels):
            if i > depth:
                break
            low = lab.lower()
            col = C["max"] if "max" in low else (C["min"] if "min" in low else C["ink2"])
            out.append(text(lx, y0 + i * dy, lab, size=12, fill=col, anchor="end", weight=700))
    out.extend(edges)
    out.extend(nodes)
    out.extend(over)
    return "\n".join(out), xend, y0 + depth * dy


def svg_doc(body, w, h, title=""):
    t = f"<title>{escape(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{t}'
            f'<rect width="{w}" height="{h}" fill="{C["bg"]}"/>{body}</svg>')


def legend_items(x, y, items, gap=26):
    """items: list of (shape, label) where shape in max|min|leaf|pv|pruned|chance|halo|tri."""
    out = []
    cx = x
    for shape, lab in items:
        if shape == "max":
            out.append(f'<rect x="{cx}" y="{y-8}" width="16" height="16" rx="3" fill="{C["max_fill"]}" stroke="{C["max"]}" stroke-width="2"/>')
        elif shape == "min":
            out.append(f'<circle cx="{cx+8}" cy="{y}" r="8" fill="{C["min_fill"]}" stroke="{C["min"]}" stroke-width="2"/>')
        elif shape == "chance":
            out.append(f'<polygon points="{cx+8},{y-9} {cx+17},{y} {cx+8},{y+9} {cx-1},{y}" fill="{C["chance_fill"]}" stroke="{C["chance"]}" stroke-width="2"/>')
        elif shape == "leaf":
            out.append(f'<rect x="{cx-2}" y="{y-9}" width="20" height="18" rx="4" fill="{C["leaf_fill"]}"/>')
        elif shape == "pv":
            out.append(f'<line x1="{cx}" y1="{y}" x2="{cx+18}" y2="{y}" stroke="{C["pv"]}" stroke-width="3.2" stroke-linecap="round"/>')
        elif shape == "pruned":
            out.append(f'<line x1="{cx-4}" y1="{y}" x2="{cx+22}" y2="{y}" stroke="{C["cut"]}" stroke-width="1.6" stroke-dasharray="5 4"/>')
            out.append(f'<circle cx="{cx+9}" cy="{y}" r="7" fill="#ffffff" stroke="{C["cut"]}" stroke-width="1.3"/>')
            out.append(f'<path d="M{cx+6},{y-3} L{cx+12},{y+3} M{cx+12},{y-3} L{cx+6},{y+3}" stroke="{C["cut"]}" stroke-width="1.8" stroke-linecap="round"/>')
        elif shape == "halo":
            out.append(f'<circle cx="{cx+8}" cy="{y}" r="8" fill="{C["new"]}" stroke="{C["halo"]}" stroke-width="2"/>')
        elif shape == "tri":
            out.append(f'<polygon points="{cx+8},{y-9} {cx+17},{y+8} {cx-1},{y+8}" fill="#fafaf8" stroke="{C["muted"]}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        elif shape == "badge":
            out.append(f'<circle cx="{cx+8}" cy="{y}" r="8.5" fill="{C["ink"]}"/>')
            out.append(text(cx + 8, y + 0.5, "k", size=10, fill="#fff", weight=700))
        out.append(text(cx + 24, y, lab, size=12.5, fill=C["ink2"], anchor="start"))
        cx += 24 + 6.9 * len(lab) + gap
    return "\n".join(out), cx


def board(x, y, s, cells, title="", hl=None, hl_color=None, sub=""):
    """3x3 tic-tac-toe board; cells is a 9-char string of X, O, '.'; hl = indices to tint."""
    out = []
    c = s / 3
    out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="#ffffff" stroke="{C["hair"]}" stroke-width="1"/>')
    if hl:
        for k in hl:
            r, q = divmod(k, 3)
            out.append(f'<rect x="{x+q*c+1}" y="{y+r*c+1}" width="{c-2}" height="{c-2}" fill="{hl_color or C["new"]}"/>')
    for i in (1, 2):
        out.append(f'<line x1="{x+i*c}" y1="{y+3}" x2="{x+i*c}" y2="{y+s-3}" stroke="{C["ink2"]}" stroke-width="1.6"/>')
        out.append(f'<line x1="{x+3}" y1="{y+i*c}" x2="{x+s-3}" y2="{y+i*c}" stroke="{C["ink2"]}" stroke-width="1.6"/>')
    for k, ch in enumerate(cells):
        r, q = divmod(k, 3)
        cx, cy = x + q * c + c / 2, y + r * c + c / 2
        m = c * 0.28
        if ch == "X":
            out.append(f'<path d="M{cx-m},{cy-m} L{cx+m},{cy+m} M{cx+m},{cy-m} L{cx-m},{cy+m}" stroke="{C["max"]}" stroke-width="{max(2,s/34):.1f}" stroke-linecap="round"/>')
        elif ch == "O":
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{m*1.05:.1f}" fill="none" stroke="{C["min"]}" stroke-width="{max(2,s/34):.1f}"/>')
    if title:
        out.append(text(x + s / 2, y - 12, title, size=12, fill=C["ink2"], weight=600))
    if sub:
        out.append(text(x + s / 2, y + s + 14, sub, size=12.5, fill=C["ink"], weight=700, family=MONO))
    return "\n".join(out)
