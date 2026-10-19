"""Week 4 charts: alpha-beta move ordering, and a Bayesian-optimisation walkthrough."""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "figures")

for f in font_manager.findSystemFonts():
    if "Inter" in os.path.basename(f) and "Display" not in f:
        font_manager.fontManager.addfont(f)

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3de", "#ffffff"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"],
    "font.size": 11,
    "svg.fonttype": "path",
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "figure.facecolor": SURF,
    "axes.facecolor": SURF,
})


def ordering_chart():
    data = json.load(open(os.path.join(HERE, "ordering_b5.json")))
    b, rows = data["b"], data["rows"]
    d = np.array([r["depth"] for r in rows])
    mm = np.array([r["minimax"] for r in rows], float)
    rnd = np.array([r["random_mean"] for r in rows])
    per = np.array([r["perfect_mean"] for r in rows])
    km = np.array([r["knuth_moore"] for r in rows], float)

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={"width_ratios": [1.45, 1]})
    fig.subplots_adjust(left=0.07, right=0.93, top=0.80, bottom=0.14, wspace=0.42)
    ax.plot(d, mm, color=INK2, lw=2, marker="o", ms=5, mec=SURF, mew=1.5, label="Minimax: every leaf ($b^d$)")
    ax.plot(d, rnd, color=BLUE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5, label="Alpha-beta, random move order")
    ax.plot(d, per, color=ORANGE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5, label="Alpha-beta, best move first")
    ax.plot(d, km, ls="none", marker="o", ms=10, mfc="none", mec=INK, mew=1.2,
            label=r"Knuth–Moore: $b^{\lceil d/2\rceil}+b^{\lfloor d/2\rfloor}-1$")
    ax.set_yscale("log")
    ax.set_xlabel("search depth d (plies)")
    ax.set_ylabel("leaves evaluated (log scale)")
    ax.set_xticks(d)
    for y, lab, col in ((mm[-1], f"{int(mm[-1]):,}", INK2), (rnd[-1], f"{int(round(rnd[-1])):,}", INK2), (per[-1], f"{int(per[-1]):,}", INK2)):
        ax.annotate(lab, (d[-1], y), xytext=(8, 0), textcoords="offset points", va="center", fontsize=10.5, color=col)
    ax.set_xlim(0.7, d[-1] + 0.9)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    ax.set_title("Leaves evaluated, uniform random trees with b = 5", loc="left", fontsize=12, color=INK, fontweight="bold")

    ebf = lambda arr: arr ** (1 / d)
    ax2.plot(d, ebf(mm), color=INK2, lw=2, marker="o", ms=5, mec=SURF, mew=1.5)
    ax2.plot(d, ebf(rnd), color=BLUE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5)
    ax2.plot(d, ebf(per), color=ORANGE, lw=2, marker="o", ms=5, mec=SURF, mew=1.5)
    ax2.axhline(math.sqrt(b), color=MUTED, lw=1)
    ax2.text(1.05, math.sqrt(b) - 0.22, r"$\sqrt{5}\approx 2.24$", color=INK2, fontsize=10)
    for arr, lab in ((ebf(mm), "minimax 5.00"), (ebf(rnd), f"random {ebf(rnd)[-1]:.2f}"), (ebf(per), f"best-first {ebf(per)[-1]:.2f}")):
        ax2.annotate(lab, (d[-1], arr[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=10, color=INK2)
    ax2.set_ylim(0, 5.6)
    ax2.set_xlim(0.7, d[-1] + 0.6)
    ax2.set_xticks(d)
    ax2.set_xlabel("search depth d (plies)")
    ax2.set_ylabel("effective branching factor (leaves$^{1/d}$)")
    ax2.set_title("Effective branching factor", loc="left", fontsize=12, color=INK, fontweight="bold")
    fig.suptitle("Move ordering decides how much alpha-beta saves", x=0.07, ha="left", y=0.97, fontsize=14, fontweight="bold", color=INK)
    fig.text(0.07, 0.885, "Mean over 30 random trees (depths 1–6) or 10 trees (depths 7–8); leaf values uniform on [0, 1]. "
             "Best-first ordering matches the Knuth–Moore count exactly.", fontsize=9.5, color=INK2)
    fig.savefig(os.path.join(OUT, "w4-17-ordering-chart.svg"))
    fig.savefig(os.path.join(HERE, "..", "figures", "w4-17-ordering-chart.png"), dpi=130)


# ---------------------------------------------------------------------------
# Bayesian optimisation with a Gaussian process (1-D), computed for real
# ---------------------------------------------------------------------------
def objective(w):
    """Hidden 'win rate' as a function of w = share of weight on the aggressive heuristic e1."""
    return 0.40 + 0.38 * np.exp(-((w - 0.62) / 0.13) ** 2) + 0.16 * np.exp(-((w - 0.18) / 0.07) ** 2) - 0.10 * w


def rbf(a, b, ls=0.11, var=0.035):
    return var * np.exp(-0.5 * (a[:, None] - b[None, :]) ** 2 / ls ** 2)


def gp_posterior(X, y, Xs, noise=1e-5, mean0=0.5):
    K = rbf(X, X) + noise * np.eye(len(X))
    Ks = rbf(X, Xs)
    Kss = rbf(Xs, Xs)
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, y - mean0))
    mu = mean0 + Ks.T @ alpha
    v = np.linalg.solve(L, Ks)
    var = np.clip(np.diag(Kss) - np.sum(v ** 2, axis=0), 1e-12, None)
    return mu, np.sqrt(var)


def expected_improvement(mu, sd, best, xi=0.005):
    from math import erf
    z = (mu - best - xi) / sd
    Phi = 0.5 * (1 + np.vectorize(erf)(z / math.sqrt(2)))
    phi = np.exp(-0.5 * z ** 2) / math.sqrt(2 * math.pi)
    return (mu - best - xi) * Phi + sd * phi


def bayesopt_chart():
    xs = np.linspace(0, 1, 600)
    fx = objective(xs)
    X = np.array([0.08, 0.92])
    y = objective(X)
    panels = []
    for it in range(4):
        mu, sd = gp_posterior(X, y, xs)
        ei = expected_improvement(mu, sd, y.max())
        nxt = xs[np.argmax(ei)]
        panels.append((X.copy(), y.copy(), mu, sd, ei, nxt))
        X = np.append(X, nxt)
        y = np.append(y, objective(nxt))
    show = [0, 1, 3]
    fig = plt.figure(figsize=(10.5, 10.2))
    gs = fig.add_gridspec(len(show) * 2, 1, height_ratios=[3, 1] * len(show), hspace=0.08)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.9, bottom=0.05)
    for k, pi in enumerate(show):
        Xo, yo, mu, sd, ei, nxt = panels[pi]
        ax = fig.add_subplot(gs[2 * k])
        ax.plot(xs, fx, color=INK2, lw=1.4, ls=(0, (5, 4)), label="true win rate (hidden: each point costs many games)")
        ax.fill_between(xs, mu - 2 * sd, mu + 2 * sd, color=BLUE, alpha=0.13, lw=0, label="uncertainty: mean ± 2 sd")
        ax.plot(xs, mu, color=BLUE, lw=2, label="surrogate model: GP posterior mean")
        ax.plot(Xo, yo, ls="none", marker="o", ms=8, mfc=INK, mec=SURF, mew=2, label="games already played (observations)", zorder=5)
        if pi > 0:
            ax.plot(Xo[-1], yo[-1], ls="none", marker="o", ms=10, mfc=ORANGE, mec=SURF, mew=2, zorder=6, label="newest observation")
        ax.set_xlim(0, 1)
        ax.set_ylim(0.1, 1.0)
        ax.set_xticklabels([])
        ax.set_ylabel("win rate")
        ax.text(0.005, 0.93, f"iteration {pi + 1}: {len(Xo)} observations", transform=ax.transAxes, fontsize=11.5, fontweight="bold", color=INK, va="top")
        if k == 0:
            ax.legend(loc="upper right", frameon=False, fontsize=9.3, ncol=1)
        ax2 = fig.add_subplot(gs[2 * k + 1])
        ax2.plot(xs, ei / ei.max(), color=ORANGE, lw=2)
        ax2.fill_between(xs, 0, ei / ei.max(), color=ORANGE, alpha=0.12, lw=0)
        ax2.axvline(nxt, color=ORANGE, lw=1)
        ax2.text(nxt + 0.01, 0.7, f"next try: w = {nxt:.2f}", color=INK2, fontsize=10)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1.15)
        ax2.set_yticks([])
        ax2.set_ylabel("acquisition\n(EI)", fontsize=9.5)
        if k < len(show) - 1:
            ax2.set_xticklabels([])
        else:
            ax2.set_xlabel("w = share of weight on the aggressive heuristic e₁   (H = w·e₁ + (1 − w)·e₂)")
    fig.suptitle("Bayesian optimisation of one heuristic weight", x=0.08, ha="left", y=0.975, fontsize=14, fontweight="bold", color=INK)
    fig.text(0.08, 0.935, "Gaussian-process surrogate with expected-improvement acquisition, computed on an illustrative win-rate curve "
             "(peak at w ≈ 0.62).", fontsize=9.8, color=INK2)
    fig.savefig(os.path.join(OUT, "w4-18-bayesopt.svg"))
    fig.savefig(os.path.join(HERE, "..", "figures", "w4-18-bayesopt.png"), dpi=120)
    print("BO trace:", [(round(float(p[5]), 3)) for p in panels], "true max at", xs[np.argmax(fx)], fx.max())
    print("observations:", np.round(X, 3), np.round(y, 3))


if __name__ == "__main__":
    ordering_chart()
    bayesopt_chart()


def hillclimb_chart():
    """Slide-36 stochastic hill climber with k = 2 heuristics, weights normalised to sum to 1.

    With w1 + w2 = 1 the weights are (w, 1 - w); a zero-mean perturbation (r, -r) moves w by eps*r.
    'H_test evaluates higher than H' = H_test wins the majority of N simulated games against H.
    """
    rng = np.random.default_rng(7)
    eps, N, iters = 0.05, 40, 120

    def run(w0):
        w = w0
        hist, acc, rej = [w], [], []
        for t in range(1, iters + 1):
            r = rng.normal()
            wt = float(np.clip(w + eps * r, 0, 1))
            p = float(np.clip(0.5 + 2.0 * (objective(wt) - objective(w)), 0.02, 0.98))
            wins = rng.binomial(N, p)
            if wins > N / 2:
                w = wt
                acc.append((t, w))
            else:
                rej.append((t, wt))
            hist.append(w)
        return np.array(hist), acc, rej

    runs = [(0.50, BLUE, "start w = 0.50"), (0.10, ORANGE, "start w = 0.10")]
    fig, ax = plt.subplots(figsize=(11, 4.6))
    fig.subplots_adjust(left=0.07, right=0.80, top=0.80, bottom=0.14)
    ax.axhline(0.618, color=INK2, lw=1)
    ax.text(iters + 2, 0.618, "global best w ≈ 0.62", va="center", fontsize=10, color=INK2)
    ax.axhline(0.18, color=MUTED, lw=1)
    ax.text(iters + 2, 0.18, "local bump w ≈ 0.18", va="center", fontsize=10, color=INK2)
    for w0, col, lab in runs:
        hist, acc, rej = run(w0)
        if rej:
            ax.plot([t for t, _ in rej], [v for _, v in rej], ls="none", marker="o", ms=3.5, mfc=MUTED, mec="none", alpha=0.45)
        ax.plot(np.arange(iters + 1), hist, color=col, lw=2, drawstyle="steps-post", label=f"{lab}, ends at {hist[-1]:.2f}")
    ax.plot([], [], ls="none", marker="o", ms=4, mfc=MUTED, mec="none", label="rejected proposals")
    ax.set_xlim(0, iters)
    ax.set_ylim(0, 1)
    ax.set_xlabel("iteration (each one = a 40-game match between H and H_test)")
    ax.set_ylabel("current weight w on e₁")
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, ncol=2)
    fig.suptitle("Stochastic hill climbing of one heuristic weight", x=0.07, ha="left", y=0.97, fontsize=14, fontweight="bold", color=INK)
    fig.text(0.07, 0.885, "Same illustrative win-rate curve as the Bayesian-optimisation figure; ε = 0.05. "
             "Noisy matches make each step a coin flip when the slope is shallow.", fontsize=9.8, color=INK2)
    fig.savefig(os.path.join(OUT, "w4-19-hillclimb.svg"))
    fig.savefig(os.path.join(HERE, "..", "figures", "w4-19-hillclimb.png"), dpi=130)


if __name__ == "__main__":
    hillclimb_chart()
