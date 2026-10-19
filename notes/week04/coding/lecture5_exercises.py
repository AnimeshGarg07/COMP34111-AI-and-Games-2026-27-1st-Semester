"""Solutions to the Lecture 5 coding exercises (run to check them)."""
from functools import lru_cache
from lecture5_minimax import MAX, MIN, CHANCE, leaf, lecture5_tree, minimax


# Exercise 1: size of a tree
def count_leaves(node):
    return 1 if node.kind == "leaf" else sum(count_leaves(c) for c in node.children)


def height(node):
    return 0 if node.kind == "leaf" else 1 + max(height(c) for c in node.children)


# Exercise 2: return the value AND the line of best play (principal variation)
def minimax_pv(node):
    if node.kind == "leaf":
        return node.payoff, [f"leaf {node.payoff}"]
    results = [minimax_pv(c) for c in node.children]
    pick = max if node.kind == "max" else min
    value, line = pick(results, key=lambda r: r[0])
    return value, [node.name] + line


# Exercise 3: Nim as an implicit game. State = (sorted heaps, player to move: 0 = MAX).
# Normal play: whoever takes the last stick wins. Pay-off +1 if MAX wins, -1 otherwise.
def nim_moves(heaps):
    for i, h in enumerate(heaps):
        for take in range(1, h + 1):
            new = list(heaps)
            new[i] -= take
            yield (i, take), tuple(sorted(new))


@lru_cache(maxsize=None)
def nim_value(heaps, to_move):
    if sum(heaps) == 0:                      # the previous player took the last stick
        return -1 if to_move == 0 else 1
    vals = [nim_value(h, 1 - to_move) for _, h in nim_moves(heaps)]
    return max(vals) if to_move == 0 else min(vals)


def nim_best(heaps):
    return [m for m, h in nim_moves(heaps) if nim_value(h, 1) == 1]


# Exercise 4: a game with dice
def dice_game():
    # MAX chooses: stop for 3, or roll a die: 1-2 -> MIN chooses between 6 and 0, 3-6 -> 5
    roll = CHANCE("roll", [(2 / 6, MIN("bad", leaf(6), leaf(0))), (4 / 6, leaf(5))])
    return MAX("root", leaf(3, "stop"), roll)


if __name__ == "__main__":
    t = lecture5_tree()
    print("Ex1 leaves:", count_leaves(t), "height:", height(t))
    print("Ex2:", minimax_pv(t))
    print("Ex3 (3,3,3) value for first player:", nim_value((3, 3, 3), 0), "winning moves:", nim_best((3, 3, 3)))
    print("    (1,2,3):", nim_value((1, 2, 3), 0), " (2,3):", nim_value((2, 3), 0), nim_best((2, 3)))
    print("Ex4 dice game value:", round(minimax(dice_game()), 4))
