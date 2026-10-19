# Week 4: minimax, alpha-beta pruning and evaluation functions

The full explanation lives in Notion (Week 4 page of the COMP34111 course database);
`Week04_Minimax_AlphaBeta_Heuristics.md` is a markdown copy of it.
This folder holds what the notes were built from, so every number in them can be re-checked.

- `figures/`: the SVG figures used in the notes.
- `code/trees.py`: minimax and a traced alpha-beta on every tree in the slides
  (Lecture 5 tree, Lecture 7 worked examples 1 and 2).
- `code/exercises.py`: the handout exercises (non-zero-sum game, 2x3 Chomp, (3,3,3)-Nim),
  tic-tac-toe counts and heuristic values, Connect-4 line count, Othello features.
- `code/ordering_experiment.py`: leaves evaluated by alpha-beta under random, best-first
  and worst-first move ordering (`python ordering_experiment.py 5 8` writes `ordering_b5.json`).
- `code/figures_trees.py`, `code/charts.py`, `code/svgtree.py`: regenerate the figures
  (`charts.py` needs numpy and matplotlib).
