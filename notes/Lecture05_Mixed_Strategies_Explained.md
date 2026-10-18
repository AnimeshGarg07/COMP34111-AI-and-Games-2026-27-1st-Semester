# COMP34111 Theory of Games, Lecture 5: Mixed Strategies (Explained Slide by Slide)

*Lecture by Jonathan Shapiro, School of Computer Science, University of Manchester.*
*These notes go through all 98 slides in order. "Slide N" means page N of the PDF. When a slide is just an animation build of the previous one (the same slide with one more bullet), I group those slides together.*

---

## How to read these notes

| Marker | Meaning |
|---|---|
| 📘 **DEFINITION** | A formal definition. You should be able to state it word for word. |
| ⭐ **KEY RESULT** | A theorem or fact that the rest of the lecture depends on. |
| 🧮 **WORKED MATHS** | A step-by-step calculation, with every step shown. |
| 💡 **INTUITION** | Why it works, in plain English. |
| ⚠️ **WATCH OUT** | A common mistake, or a typo or inconsistency on the slide. |
| 🎯 **EXAM TIP** | What is likely to be asked, and how to answer it. |
| ➕ **BEYOND THE SLIDES** | Extra context that is not on the slides. It helps understanding but is probably not examined directly. |

---

## TL;DR: the whole lecture in 6 lines

1. Some games (matching pennies, poker, Rock-Paper-Scissors) have **no pure-strategy equilibrium**: whoever is predictable gets exploited.
2. The fix is a **mixed strategy**: a probability distribution over your pure strategies.
3. ⭐ **Nash's theorem:** once mixing is allowed, *every* finite game has at least one Nash equilibrium.
4. ⭐ **Indifference principle:** at a mixed equilibrium, each player mixes so that the **opponent** gets the same expected payoff from every pure strategy they use. If the opponent is indifferent, they cannot gain by deviating.
5. For 2-player zero-sum games, this "equalising" point is exactly the **maximum of the minima** (max-min) in the space of mixed strategies. For 2×2 games you can find it **graphically** (where the two lines cross).
6. Three worked examples: **Brothers/cafés** gives (½, ½) with value 0. **Tiny poker** gives "always bet with W, bluff ⅓ with L, call ⅔", with value ⅓ to the bettor. **RPS with a 1000 prize** gives (1/1002, 1000/1002, 1/1002), so you almost always play Paper.

---

## Lecture map

| Part | Slides | Topic |
|---|---|---|
| 0 | 1–3 | Admin and reading |
| 1 | 4–8 | Recap of Lecture 4: best response, Nash equilibrium, mini-max, dominance |
| 2 | 9 | The problem: a game with no pure-strategy solution |
| 3 | 10–15 | Mixed strategies: definition, extensive form, when they are needed, Nash's theorem, algorithms |
| 4 | 16–45 | Example 1: big brother / little brother (matching pennies) |
| 5 | 46–80 | Example 2: 2-card "tiny poker" (why bluffing is rational) |
| 6 | 81–97 | Example 3: generalised Rock-Paper-Scissors |
| 7 | 98 | Conclusions |
| – | – | Errata, cheat sheet, self-test questions (at the end) |

---

# Part 0: Admin (Slides 1–3)

### Slide 1: Attendance
This slide is only for taking attendance. The "attendance" button on the last slide (98) links back here. There is no content.

### Slide 2: Title
*"The theory of games, Lecture 5."* Jonathan Shapiro, School of Computer Science, University of Manchester.

### Slide 3: Readings
- **Reading for today:** pp. 40–60 of the course notes (proofs optional).
- **Simplified poker:** Section 2.7 solves a *more complex* version of the poker game in this lecture.
- **Reading notes:** finish Chapter 2.

🎯 **EXAM TIP:** Section 2.7 is good practice. It uses exactly the same method as slides 57–79, just on a bigger game.

---

# Part 1: Recap of Lecture 4 (Slides 4–8)

These five slides remind you of the tools from last time. The lecture then shows where those tools break down (slide 9) and how mixed strategies fix them.

### Slide 4: Best response strategy

📘 **DEFINITION:** *A **best response strategy** is the strategy for a given player which yields the highest payoff to that player, with the strategies of all the other players held fixed.*

**Explanation:**
- "With the others held fixed" means you treat your opponents' choices as given and ask: *"Given what they are doing, what is the best thing I can do?"*
- So a best response is always **relative**: it is a function of what the other players do. In symbols, BR₁(s₂) = the s₁ that maximises U₁(s₁, s₂).
- **Example** (using the matrix on slide 9): if Column plays A, Row's best response is row 2 (payoff +1 instead of −1). If Column plays B, Row's best response is row 1.

➕ **BEYOND THE SLIDES:** A player can have **several** best responses at once when there is a tie. This matters a lot in this lecture. At a mixed equilibrium, *every* pure strategy in the mix is a best response, because they all give the same payoff.

### Slide 5: Nash equilibrium
*(Definition on page 31 of the notes.)*
- Each player is playing a **best response to all the others**.
- It is **not a strategy**. It is a **choice of strategy for *all* players** in the game (a *strategy profile*).
- If the players are playing the Nash, **no player has any incentive to change its strategy *unilaterally***.

📘 **DEFINITION (formal, 2 players):** A profile (s₁\*, s₂\*) is a Nash equilibrium if and only if
- U₁(s₁\*, s₂\*) ≥ U₁(s₁, s₂\*) for every strategy s₁ of player 1, **and**
- U₂(s₁\*, s₂\*) ≥ U₂(s₁\*, s₂) for every strategy s₂ of player 2.

💡 **INTUITION:** "Unilaterally" means *on your own*, with everyone else keeping their strategy. A Nash equilibrium is a **"no regrets"** point: after seeing what everyone did, nobody wishes they alone had done something different. It is a statement about **stability**, not about the outcome being good. In the Prisoner's Dilemma, for example, the equilibrium is bad for both players.

⚠️ **WATCH OUT:** Don't write *"player 1's Nash equilibrium is X"*. An equilibrium is a **profile**, so write *"(X, Y) is a Nash equilibrium"*.

### Slide 6: Mini-max approach
For **2-player, zero-sum games in normal form**:
- **Player 1** (the maximiser) finds the **minimum** payoff for each of its strategies (the row minimum), then plays the strategy that **maximises** that minimum. This gives the **max-min** (maximin) value.
- **Player 2** (the minimiser) finds the **maximum** payoff to Player 1 for each of its strategies (the column maximum), then plays the strategy that **minimises** it. This gives the **min-max** (minimax) value.
- *"If such a pair of strategies exists, they constitute a Nash equilibrium."*

**What "if such a pair exists" means:** the procedure always gives *some* pair of strategies. The question is whether the pair is **consistent**, i.e. whether **max-min = min-max**. It is always true that max-min ≤ min-max. When they are **equal**, the cell where they meet is a **saddle point**. The saddle point is a pure Nash equilibrium, and the common number is the **value of the game**.

🧮 **WORKED MATHS (a game *with* a saddle point):**

| | C1 | C2 | row min |
|---|---|---|---|
| **R1** | 3 | 5 | **3** ← max of the row minima |
| **R2** | 1 | 4 | 1 |
| **column max** | **3** ← min of the column maxima | 5 | |

Max-min = 3 = min-max, so (R1, C1) is a saddle point and the value is 3. Check: the 3 is the smallest number in its row *and* the largest number in its column, so neither player wants to move.

### Slide 7: Mini-max is a worst-case analysis
From the perspective of **both** players:
- for each of my strategies, find **the most harm my opponent can do to me**;
- choose the strategy which makes that **least bad**.

💡 **INTUITION:** Mini-max is a pessimistic, "assume the opponent is clever" way of thinking. In a **zero-sum** game the pessimism is justified: whatever is bad for you is *exactly* good for your opponent, so a rational opponent *is* trying to hurt you.

This idea comes back at slide 31, where the mixed equilibrium turns out to be *"the maximum of the minima in mixed-strategy space"*. It is the same worst-case reasoning, applied to probabilities instead of rows.

### Slide 8: Dominance
*"We also saw how the concept of dominance could be used to remove strategies from consideration."*
- Strategy A **dominates** strategy B if the payoffs of A are better than or no worse than the payoffs of B, ***independent of what the opponent does***.
- **Dominated strategies can be removed.**

📘 **DEFINITION (precise):**
- **Strict dominance:** A gives a strictly higher payoff than B against **every** opponent strategy.
- **Weak dominance:** A is ≥ B against every opponent strategy, and strictly > against at least one.

The slide's wording ("better or no worse") describes **weak** dominance.

⚠️ **WATCH OUT:** Removing **strictly** dominated strategies never removes a Nash equilibrium. Removing **weakly** dominated ones *can* remove some equilibria, and the order of removal can matter.

This tool is used again at **slide 58**: "B_W¹ = 1 by dominance".

---

# Part 2: The problem (Slide 9)

### Slide 9: Next topic: games with no *apparent* mini-max solution

| Row \ Column | A | B |
|---|---|---|
| **1** | (−1, 1) | (1, −1) |
| **2** | (1, −1) | (−1, 1) |

Each cell is *(payoff to Row, payoff to Column)*. Every cell sums to 0, so the game is **zero-sum**. This classic game is called **matching pennies**.

*"Does this have a mini-max solution? Does it have a Nash equilibrium? We will answer these questions."*

🧮 **WORKED MATHS: try the mini-max method from slide 6** (using Row's payoffs):
- Row minima: row 1 gives min(−1, 1) = −1. Row 2 gives min(1, −1) = −1. So **max-min = −1**.
- Column maxima: column A gives max(−1, 1) = 1. Column B gives max(1, −1) = 1. So **min-max = +1**.
- Max-min (−1) ≠ min-max (+1), so there is **no saddle point and no pure mini-max solution.**

🧮 **WORKED MATHS: check every cell for a pure Nash equilibrium:**
- (1, A): Row gets −1. Switching to row 2 gives +1, so Row deviates. **Not a NE.**
- (1, B): Column gets −1. Switching to A gives +1, so Column deviates. **Not a NE.**
- (2, A): Column gets −1. Switching to B gives +1. **Not a NE.**
- (2, B): Row gets −1. Switching to row 1 gives +1. **Not a NE.**

The best responses **cycle forever**: Row plays 1, so Column moves to A, so Row moves to 2, so Column moves to B, so Row moves back to 1, and so on.

**The answers to the slide's questions:**
- A mini-max solution in pure strategies? **No.**
- A Nash equilibrium in pure strategies? **No.**
- A Nash equilibrium **at all**? **Yes, in mixed strategies:** both players play each option with probability ½ (shown on slides 40–43). That is why the slide says no *apparent* solution.

---

# Part 3: Mixed strategies (Slides 10–15)

### Slides 10–11: Mixed strategies in normal form

📘 **DEFINITION:** A **mixed strategy** is a strategy for a player in which the player:
- plays a **probabilistic combination of pure strategies**;
- receives a **probabilistic combination of payoffs**.

**In normal form:**
- Assign probability **qᵢ** to the pure strategy **i**,
- where **0 ≤ qᵢ ≤ 1** and **Σᵢ qᵢ = 1** (so the qᵢ form a probability distribution).
- Choose strategy i with probability qᵢ.
- Get the corresponding payoff with probability qᵢ.

💡 **INTUITION:** Before you play, you privately roll a die or spin a spinner, and the result decides which pure strategy you use. The opponent knows your *probabilities* but not the *outcome* of your spin.

**Important consequences:**
- A **pure** strategy is just a special mixed strategy: q = 1 on one strategy and 0 on all the others.
- With **2 pure strategies**, a mixed strategy is a **single number** x ∈ [0, 1] (the probability of the first strategy; the second gets 1 − x). This is why every 2×2 example in this lecture can be **drawn as a graph** over the interval [0, 1].
- **Example:** in Rock-Paper-Scissors, (q_R, q_P, q_S) = (⅓, ⅓, ⅓).

### Slide 12: Mixed strategies in extensive form
- **Extensive form:** *at each node where the player has a decision, assign a probability to each of the possible choices.*

**Reading the diagram on the slide:**
- The **root** branches to nodes **b, c, d** with probabilities **0.8, 0.1, 0.1**. These are chosen by whoever moves at the root, which could be chance or another player.
- **b, c, d** are decision nodes of the player we care about. The **dotted box** labelled *"information set"* means the player **cannot tell which of b, c or d they are at**.
- At each of b, c and d the player chooses left with probability **0.1** and right with probability **0.9** (b leads to e/f, c to g/h, d to i/j).

⚠️ **WATCH OUT: the most important detail of this diagram.** The probabilities are the **same (0.1 / 0.9) at b, c and d.** This is not a coincidence. The player can't tell those nodes apart, so they **can't behave differently at them**. A strategy assigns one choice (or one probability distribution) per **information set**, not per node.

➕ **BEYOND THE SLIDES:** Randomising independently at each information set is technically called a **behavioural strategy**. Randomising over complete plans ("whole pure strategies") is a **mixed strategy**. **Kuhn's theorem** says the two are equivalent in games with *perfect recall* (players never forget what they knew or did), which is why the slides treat them as the same idea.

### Slide 13: When mixed strategies are needed
*Mixed strategies can be required when there is **hidden information**:*
- **Extensive-form games with hidden information** (e.g. poker).
- **Normal-form games always have hidden information**: the opponent's strategy is hidden, because moves are made simultaneously.

💡 **INTUITION:**
- In a **perfect-information** game (chess, noughts and crosses), you always know exactly where you are. **Backward induction** then gives an optimal **pure** strategy, so randomising can never help you.
- When information is **hidden**, **being predictable is a weakness**: if your opponent can predict you, they can exploit you. Randomising makes you unpredictable.
- A normal-form game is like both players writing their move in a sealed envelope. Neither sees the other's choice, so information is hidden by construction.

### Slide 14: Mixed-strategy Nash equilibria
- Mixed strategies are probabilistic combinations of pure strategies.
- ⭐ **KEY RESULT: Nash (1950).** *All games with a finite number of players and a finite number of moves have **at least one Nash equilibrium** (mixed or pure).*

💡 **INTUITION:** This is *why* mixed strategies matter. Without them, matching pennies and Rock-Paper-Scissors would have no equilibrium at all. Allowing mixing "fills in the gaps" and **guarantees** that an equilibrium exists.

⚠️ **WATCH OUT:**
- The theorem says **"at least one"**. A game may have many equilibria.
- The equilibrium may be **mixed**. The claim *"every finite game has a pure Nash equilibrium"* is **false**, and slide 9 is a counterexample.

➕ **BEYOND THE SLIDES:**
- Nash's proof uses a **fixed-point theorem** (Brouwer's or Kakutani's). It is not needed here ("proofs optional").
- For 2-player **zero-sum** games there is an earlier result, **von Neumann's minimax theorem (1928)**: in mixed strategies, **max over x of min over y = min over y of max over x**. Max-min always equals min-max once mixing is allowed. You will see this happen graphically on slides 32–39.

### Slide 15: Finding Nash equilibria in the general case
- **General-sum games:** the best algorithm seems to be the **Lemke–Howson algorithm** (for 2-player games), which **can be exponential in time**.
- **Zero-sum games in normal form:** can generally be solved using **linear programming** (polynomial time).
- *"We will look at simple cases. The full tools of linear programming are not required."*

➕ **BEYOND THE SLIDES: the linear program for player 1** (A is Row's payoff matrix, x is Row's mixed strategy):

```
maximise    v
subject to  Σᵢ xᵢ · A[i][j] ≥ v     for every column j   (against EVERY opponent pure strategy I get ≥ v)
            Σᵢ xᵢ = 1,  xᵢ ≥ 0                          (x is a probability distribution)
```

In words: *choose a mix x that guarantees at least v whatever the opponent does, and make v as large as possible.* That is "maximise the minimum" written as a linear program.

➕ **BEYOND THE SLIDES:** Computing a Nash equilibrium in general games is **PPAD-complete**, which is believed to be hard. That is why no fast general algorithm is known.

🎯 **EXAM TIP:** In this course you solve things **by hand**. For 2×2 games, use the **graphical method** or the **indifference equations**. For small n×n games, solve a **system of linear equations** (as in the RPS example on slides 85–97).

---

# Part 4: Example 1, big brother / little brother (Slides 16–45)

### Slides 16–17: The game
- Two brothers, **Donald** (older) and **Eric** (younger), go to the same high school.
- The school has two cafés, **Red** and **Blue**, where they eat lunch every day.
- **Donald wants to be in a different café** from his little brother,
- **but Eric always wants to be near his big brother.**

**Payoff matrix**, each cell is *(Donald, Eric)*:

| Donald \ Eric | Red | Blue |
|---|---|---|
| **Red** | (−1, 1) | (1, −1) |
| **Blue** | (1, −1) | (−1, 1) |

**Reading it:**
- **Same café** (the diagonal): Eric is happy (+1) and Donald is annoyed (−1).
- **Different cafés** (off the diagonal): Donald is happy (+1) and Eric is sad (−1).
- The game is zero-sum, and it is **exactly the slide 9 matrix** with the labels changed (Row = Donald, 1 = Red, A = Red). Solving this game therefore also answers slide 9.

💡 **INTUITION: why there is no pure solution:** if Donald is predictable, Eric follows him. If Eric is predictable, Donald avoids him. **Whoever is predictable loses**, so both must randomise.

### Slide 18: The mixed strategies
Each brother chooses his lunch spot **probabilistically and independently**:
- **Donald:** Red café with probability **x**, Blue café with probability **1 − x**.
- **Eric:** Red café with probability **y**, Blue café with probability **1 − y**.

So Donald's whole strategy is one number x ∈ [0, 1], and Eric's is one number y ∈ [0, 1]. (x = 1 means "always Red", which is a pure strategy.)

### Slides 19–22: Expected payoff (built up one bullet at a time)
- Since the strategies are probabilistic, **so are the payoffs**.
- So we need the **expected payoffs**.
- Let **U₁(S₁, S₂)** be the payoff to Player 1 for a given pair of pure strategies (S₁, S₂). Likewise **U₂(S₁, S₂)** for Player 2.
- **Expected (average) payoff:** **Ex[U₁(S₁, S₂)]**, for pure or mixed strategies (S₁, S₂).

📘 **DEFINITION:** expected payoff = Σ over all outcomes of (probability of the outcome × payoff of the outcome). Because the two players randomise **independently**, P(Donald plays i **and** Eric plays j) = P(Donald plays i) × P(Eric plays j).

💡 **INTUITION:** "Average" is the right word. The brothers eat lunch **every day**, so over many days Donald's average daily payoff converges to the expected payoff (by the law of large numbers).

➕ **BEYOND THE SLIDES: the full expected payoff to Donald as a function of both x and y:**

```
E[U₁(x, y)] = (−1)·x·y + (+1)·x·(1−y) + (+1)·(1−x)·y + (−1)·(1−x)·(1−y)
            = 2x + 2y − 4xy − 1
            = −(2x − 1)(2y − 1)
```

So E[U₂(x, y)] = +(2x − 1)(2y − 1). Look what happens when **x = ½**: the factor (2x − 1) = 0, so **Donald's payoff is 0 no matter what Eric does**. This is the indifference principle (next slide) appearing directly in the algebra.

### Slide 23: A basic principle (the most important slide of the lecture)
- Player 1 chooses its mixed strategy such that **Player 2 gets the same payoff whichever action it takes**.
- Player 2 chooses its mixed strategy such that **Player 1 gets the same payoff whichever action it takes**.
- *Then it will be a Nash equilibrium!*

⭐ **KEY RESULT: the INDIFFERENCE PRINCIPLE.**

⚠️ **WATCH OUT: the most common confusion in this topic.** You choose **YOUR** probabilities to make **your OPPONENT** indifferent, not yourself.
- Donald's x is pinned down by **Eric's** payoffs.
- Eric's y is pinned down by **Donald's** payoffs.
- In **zero-sum** games this makes no practical difference, because U₂ = −U₁. "Make Eric indifferent" is the same as "make Donald's own payoff equal against Eric's Red and Eric's Blue". In **general-sum** games the distinction really matters.

💡 **INTUITION: why indifference gives a Nash equilibrium:** if Eric is indifferent between Red and Blue, **every** mix y gives him the same payoff. So his current y is a best response, because nothing does better. The same holds for Donald. Both players are best-responding, which is the definition of a Nash equilibrium (slide 5).

### Slide 24: Optimal choice for Donald
To find the optimal value of x for Donald:
1. **Find the expected payoffs against each of the opponent's pure strategies** (each one a function of x).
2. **Find the mixed strategy x which makes them equal.**

### Slides 25–26: Optimizing Donald's decision

🧮 **WORKED MATHS:**

**If Eric always goes to the Red café:**

```
Ex[U₂(S₁(x), Red)] = (1)·x + (−1)·(1 − x)        (1)
                   = 2x − 1                       (2)
```

*Why:* with probability x Donald is also at Red. They are in the same café, so Eric gets +1. With probability 1 − x Donald is at Blue, so Eric gets −1.

**If Eric always goes to the Blue café:**

```
Ex[U₂(S₁(x), Blue)] = (−1)·x + (1)·(1 − x)       (3)
                    = 1 − 2x                      (4)
```

*Why:* with probability x Donald is at Red (different café), so Eric gets −1. With probability 1 − x Donald is at Blue (same café), so Eric gets +1.

**Task: set them equal.**

```
2x − 1 = 1 − 2x   ⟹   4x = 2   ⟹   x = ½     (boxed on slide 26)
```

**Check:** at x = ½, Eric gets 2(½) − 1 = 0 from Red and 1 − 2(½) = 0 from Blue. He is indifferent ✓.

⚠️ **WATCH OUT (typo on slide):** the "Task" line writes Ex[U₂(**S₂**(x), Red)]. It should be **S₁(x)**, because x is Donald's (player 1's) parameter.

⚠️ **WATCH OUT (not a typo):** the slide is titled *"Donald's decision"* but it computes **U₂, Eric's payoff**. This is deliberate. It is the indifference principle: Donald chooses x to make **Eric** indifferent.

**The same calculation for Eric** (not shown on this slide; the result appears on slide 40). Eric chooses y to make **Donald** indifferent:

```
Ex[U₁(Red,  S₂(y))] = (−1)·y + (1)·(1 − y) = 1 − 2y
Ex[U₁(Blue, S₂(y))] = (1)·y + (−1)·(1 − y) = 2y − 1
1 − 2y = 2y − 1   ⟹   y = ½
```

### Slides 27–29: Why must the expected payoffs be equal?
- **If they are not equal:** Eric will have a **pure-strategy best response which will be higher**. He would put 100% on the better option.
- **If they are equal:** Eric gets **the same payoff whatever strategy he uses**.
- **Why?** *(the slide leaves this for you)*
- So Eric will have **no incentive to unilaterally deviate** from whatever he does.

🧮 **The answer to "Why?":** any strategy Eric could use is some mix y of Red and Blue, so his expected payoff is a **weighted average**:

```
E[U₂] = y · E[U₂ | Red] + (1 − y) · E[U₂ | Blue]
```

If E[U₂ | Red] = E[U₂ | Blue] = v, then E[U₂] = y·v + (1 − y)·v = **v for every y**. An average of equal numbers is just that number. No choice of y does better, so Eric has nothing to gain by changing.

**And if they are unequal**, say E[U₂ | Red] > E[U₂ | Blue], then E[U₂] increases with y and is maximised at y = 1 (always Red). Eric goes pure, Donald then reacts, and the cycle starts (next slide).

### Slide 30: "Mathematical" (the cycling argument)
- Let S₁(x) be Donald's strategy (a function of x).
- Let Eric use a pure strategy: Red or Blue.
- Suppose the expected payoff **to Donald** is bigger when Eric plays Red than when he plays Blue.
- Then **Eric should play Blue** against S₁(x). (Zero-sum: Eric wants Donald's payoff to be *low*.)
- Then **Donald should play Red** against Eric's Blue. (Donald wants a different café.)
- ⋮ *(The dots mean: then Eric switches to Red, so Donald switches to Blue, so Eric switches to Blue, and so on forever.)*

**Conclusion:** the only way to stop this cycle is for the payoffs to be **equal**, so that nobody has a strictly better pure reply.

⚠️ **WATCH OUT (notation slip on slide):** the text says *"payoff **to Donald**"* but the formula is written with **U₂** (Eric's payoff). For the argument to work it should read Ex[**U₁**(S₁(x), Red)] > Ex[**U₁**(S₁(x), Blue)]. Equivalently, keep U₂ and flip the inequality to "<".

### Slide 31: Relation to mini-max
*"This is the **maximum of the minima** in mixed-strategy space."*

💡 **INTUITION:**
- For any x Donald might pick, Eric will choose whichever reply hurts Donald most. Donald's **worst-case** payoff for that x is therefore **min{ payoff if Eric goes Red, payoff if Eric goes Blue }**.
- Donald picks x to **maximise that worst case**. This is exactly the mini-max reasoning of slides 6–7, except that x now ranges over **every number in [0, 1]** instead of just "row 1 or row 2".
- One line rises with x and the other falls, so their minimum looks like a tent (Λ), and **the top of the tent is where the two lines cross**, i.e. where the payoffs are **equal**.
- So *"equalise the payoffs"* and *"maximise the minimum"* give **the same answer**. Slides 32–39 show this with graphs.

### Slides 32–35: Graphical depiction (Donald's point of view)

**Axes:** horizontal = **x**, the probability Donald goes Red (0 to 1). Vertical = **expected payoff to Donald**.

- **Slide 32, blue line, "Eric plays Red Cafe":** payoff to Donald = (−1)x + (1)(1 − x) = **1 − 2x**. It falls from +1 (at x = 0) to −1 (at x = 1). If Eric is at Red, Donald does best by never going to Red.
- **Slide 33, orange line, "Eric plays Blue Cafe":** payoff to Donald = (1)x + (−1)(1 − x) = **2x − 1**. It rises from −1 to +1.
- The lines **cross at x = ½, payoff 0**.
- **Slide 34, thick green line, "Minimum":** this is the **lower envelope** min(1 − 2x, 2x − 1), which equals −|2x − 1|. It is Donald's **guaranteed** payoff for each x, because Eric will pick whichever line is lower. It has a **Λ (tent) shape**.
- **Slide 35, red star, "max of the min":** the highest point of the green tent is at **x = ½, payoff 0**. The dashed lines read off x = ½ on the horizontal axis and 0 on the vertical axis.

🧮 **The same picture as a table:**

| x (Donald's P(Red)) | Eric plays Red: 1 − 2x | Eric plays Blue: 2x − 1 | Donald's worst case = min |
|---|---|---|---|
| 0 | 1 | −1 | −1 |
| 0.25 | 0.5 | −0.5 | −0.5 |
| **0.5** | **0** | **0** | **0 ← maximum** |
| 0.75 | −0.5 | 0.5 | −0.5 |
| 1 | −1 | 1 | −1 |

### Slides 36–39: Graphical depiction from Eric's point of view

**Axes:** horizontal = **y**, the probability Eric goes Red. Vertical = still the **expected payoff to Donald**. Because the game is zero-sum, Eric's payoff is just the negative of this, so **Eric wants this number to be LOW**.

- **Slide 36, blue line, "Donald plays Red Cafe":** payoff to Donald = (−1)y + (1)(1 − y) = **1 − 2y**. It falls from +1 to −1. If Donald is at Red, Eric hurts Donald more by going to Red more often.
- **Slide 37, orange line, "Donald plays Blue Cafe":** payoff to Donald = (1)y + (−1)(1 − y) = **2y − 1**. It rises.
- **Slide 38, thick green line, "Maximum":** the **upper envelope** max(1 − 2y, 2y − 1), which equals |2y − 1|. It is the **worst case for Eric**, because Donald will pick the higher line. It has a **V shape**.
- **Slide 39, red star, "min of the max":** Eric minimises the maximum, so he picks the **bottom of the V at y = ½, payoff 0**.

| y (Eric's P(Red)) | Donald plays Red: 1 − 2y | Donald plays Blue: 2y − 1 | Eric's worst case = max |
|---|---|---|---|
| 0 | 1 | −1 | 1 |
| 0.25 | 0.5 | −0.5 | 0.5 |
| **0.5** | **0** | **0** | **0 ← minimum** |
| 0.75 | −0.5 | 0.5 | 0.5 |
| 1 | −1 | 1 | 1 |

⭐ **KEY RESULT (the minimax theorem in action):** Donald's **max of the min** = 0 = Eric's **min of the max**. In pure strategies these two numbers were −1 and +1 (slide 9). Once mixing is allowed they **become equal**, and the common value **0 is the value of the game**.

### Slides 40–43: The Nash equilibrium
- **x = ½ and y = ½.**
- Donald and Eric both choose their lunch café **independently with a random probability of 0.5** (for example, each flips a coin every morning).
- They are each **happy half the time and unhappy half the time, on average.**
- **Neither has an incentive to unilaterally deviate, because *their payoff will not change*.**

🧮 **WORKED MATHS:** P(same café) = xy + (1 − x)(1 − y) = ¼ + ¼ = **½**. So Eric is happy half the time and Donald is happy half the time. Each has expected payoff ½(+1) + ½(−1) = **0**.

⚠️ **WATCH OUT (subtle):** at a mixed equilibrium, deviating does not make you *worse off* against the opponent's equilibrium strategy. It just doesn't make you *better off*, and "no strict improvement" is all that the Nash definition requires. **But** a deviation would leave you open to **exploitation** if the opponent adapted. That is the point of slide 44.

➕ **BEYOND THE SLIDES: the best-response picture**
- **Donald's** best response to y: if y > ½ (Eric mostly Red), Donald goes Blue (x = 0). If y < ½, he goes Red (x = 1). If y = ½, any x is a best response.
- **Eric's** best response to x: if x > ½, Eric goes Red (y = 1). If x < ½, he goes Blue (y = 0). If x = ½, any y is a best response.
- The **only** point where each is a best response to the other is **(½, ½)**, so the equilibrium is **unique**.

### Slide 44: A key property of the solution
*A common feature of mixed-strategy Nash equilibria:*
1. If one player plays its component of the *mixed* Nash equilibrium, the payoff is **indifferent to what the other player does**.
2. The other player **must also play its component** of the Nash equilibrium, to **force the first player to play its component and not take advantage**.

*(The slide has a small typo: "component of the of the".)*

💡 **INTUITION:**
- **Point 1:** if Donald plays x = ½, Eric's choice doesn't matter. He gets 0 whatever he does.
- **Point 2:** so why should Eric bother playing exactly ½? Suppose Eric plays y = 0.7 (Red more often). Then Donald is **no longer indifferent**. His best response becomes "always Blue" (x = 0), which earns Donald 0.7(+1) + 0.3(−1) = **+0.4 > 0**. Eric's y = ½ is precisely what **keeps Donald indifferent** and stops him from exploiting Eric.
- In other words, **each player's mix protects them**: it removes the opponent's incentive to deviate.

🎯 **EXAM TIP:** A classic question is *"At a mixed Nash equilibrium each player is indifferent between their pure strategies. Why, then, must they play the specific equilibrium mix?"* The answer is point 2 above. Their mix is what keeps the **opponent** indifferent. Change it, and the opponent gets a strictly better pure response that exploits you.

### Slide 45: Key ideas
1. **Introduce probabilities** over pure strategies.
2. **Set the expected payoffs** against each of the opponent's pure strategies **equal**, and solve for the probabilities.
3. With 2-action, 2-player games, Nash equilibria can be **found graphically**.

🎯 **EXAM TIP: a step-by-step recipe for a 2×2 zero-sum game:**
- **Step 0.** Check for a **saddle point** (pure solution: max-min = min-max). Remove any **dominated** strategies.
- **Step 1.** Let x = P(Row plays row 1). Write Row's expected payoff against **column 1** and against **column 2** as functions of x.
- **Step 2.** Set them **equal** and solve for x.
- **Step 3.** Do the same for Column: let y = P(column 1), and set Row's payoff from **row 1** equal to Row's payoff from **row 2**.
- **Step 4.** Substitute back to get the **value**. Check 0 ≤ x, y ≤ 1. If not, you missed a saddle point or a dominated strategy.

➕ **BEYOND THE SLIDES: closed-form formula for a 2×2 zero-sum game with no saddle point.** If Row's payoffs are `[[a, b], [c, d]]` (row 1 = a, b; row 2 = c, d), then:

```
D  = a − b − c + d
x* = P(Row plays row 1)    = (d − c) / D
y* = P(Col plays column 1) = (d − b) / D
value                      = (ad − bc) / D
```

**Check on the brothers game** (Donald's payoffs a = −1, b = 1, c = 1, d = −1): D = −4, so x* = (−1 − 1)/(−4) = ½ ✓, y* = (−1 − 1)/(−4) = ½ ✓, and value = (1 − 1)/(−4) = 0 ✓.

---

# Part 5: Example 2, 2-player 2-card "tiny poker" (Slides 46–80)

### Slide 46: The rules
**Equipment:** a deck of cards with two types of card, **W** and **L**.
1. Each player puts **£1 into the pot** (the "ante"). The pot is now £2.
2. **Player 1 draws a card** from the deck but **does not show it** to Player 2.
3. Player 1 can then **bet or fold**. If he **folds**, Player 2 gets the pot. If he **bets**, he puts **another £1** into the pot (pot = £3).
4. If Player 1 bet, **Player 2 can call or fold**. If he **folds**, Player 1 gets the pot.
5. If Player 2 **calls**, he puts **another £1** into the pot (pot = £4). There is a **showdown**, and Player 1 must show his card.
6. **W** means Player 1 wins. **L** means Player 2 wins.

⚠️ **WATCH OUT (hidden assumption):** the calculations later (the factor ½ on slides 74–79) assume **W and L are equally likely**, each with probability ½.

🧮 **WORKED MATHS: net payoff to Player 1** (money gained or lost compared with before the game):

| Card | P1 does | P2 does | Net to P1 | Why |
|---|---|---|---|---|
| W or L | fold | – | **−1** | loses his £1 ante |
| W or L | bet | fold | **+1** | wins P2's £1 ante |
| W | bet | call | **+2** | wins P2's ante + P2's call |
| L | bet | call | **−2** | loses his ante + his bet |

The game is zero-sum, so Player 2's payoff is always the negative of Player 1's.

### Slides 47–52: The game tree
**Reading the tree:**
- The **diamond "chance"** node at the top is *nature* dealing the card: **W** or **L** (½ each).
- The **square "Player 1"** nodes: there is one after W and one after L. Player 1 **knows his card**, so these are **separate information sets**, and **Player 1 can act differently with W and with L**.
  - **fold** leads to a leaf with **−1** on both sides.
  - **bet** leads to a Player 2 node.
- The **oval "Player 2"** nodes. From slide 48 onward they are enclosed in a **blue box labelled "information set"**: Player 2 **sees that P1 bet, but not P1's card**. So Player 2 **cannot tell which of the two nodes it is at**, and must use the **same action (or the same probabilities)** at both.
- **Leaves:**
  - W branch: P2 folds gives **1**, P2 calls gives **2**.
  - L branch: P2 calls gives **−2**, P2 folds gives **1**.
- **Slides 49 and 52:** *"This is a **two-player, zero-sum game with chance and imperfect information**."*
  - two-player: Teacher and Student;
  - zero-sum: whatever P1 wins, P2 loses;
  - **chance**: the random deal;
  - **imperfect information**: P2 doesn't see the card (that is what the information set means).
- **Slide 50** is blank except for *"The following slide is for handouts only"*. **Slides 51–52** repeat the tree for the printed handout, because the purple "Continue" buttons are clickable links in the live presentation. There is no new content.

➕ **BEYOND THE SLIDES: why the information set changes everything.** Suppose P2 **could** see the card. Then the game would have perfect information and backward induction would solve it:
- With W, P2 folds (lose 1 rather than 2). With L, P2 calls (win 2 rather than lose 1).
- P1 then bets with W (+1 instead of −1) and folds with L (−1 instead of −2).
- The value would be ½(+1) + ½(−1) = **0**.

The **hidden card** is what creates both the need and the opportunity for **bluffing**, and it raises P1's value from 0 to ⅓ (shown below).

### Slide 53: Tiny poker in normal form
**Teacher = Player 1, Student = Player 2.** (The lecturer played this game against the class.)
- The Teacher has **4 pure strategies**: one action at each of his **2 information sets** (holding W, holding L), giving 2 × 2 = 4.
- The Student has **2 pure strategies**: one action at its **1 information set**. "Always bet" for the student means **always call**.

Entries are the **expected payoff to the Teacher**, averaged over the deal:

| Teacher \ Student | Always bet (call) | Always fold |
|---|---|---|
| **Bet with W; Bet with L** | 0 | 1 |
| **Bet with W; Fold with L** | ½ | 0 |
| **Fold with W; Bet with L** | −3/2 | 0 |
| **Fold with W; Fold with L** | −1 | −1 |

🧮 **WORKED MATHS: where every entry comes from** (½ × [payoff with W] + ½ × [payoff with L]):

| Teacher strategy | vs call | vs fold |
|---|---|---|
| Bet W, Bet L | ½(+2) + ½(−2) = **0** | ½(+1) + ½(+1) = **1** |
| Bet W, Fold L | ½(+2) + ½(−1) = **½** | ½(+1) + ½(−1) = **0** |
| Fold W, Bet L | ½(−1) + ½(−2) = **−3/2** | ½(−1) + ½(+1) = **0** |
| Fold W, Fold L | ½(−1) + ½(−1) = **−1** | ½(−1) + ½(−1) = **−1** |

💡 **INTUITION:** this is how you **convert extensive form to normal form**. A pure strategy is a **complete plan** saying what you would do at *every* information set, and the chance move is **averaged out**.

🧮 **WORKED MATHS: simplify with dominance** (slide 8):
- "Bet W, Bet L" gives (0, 1) and "Fold W, Bet L" gives (−3/2, 0). The first is **better in both columns**, so *Fold W, Bet L* is **dominated**.
- "Bet W, Fold L" gives (½, 0) and "Fold W, Fold L" gives (−1, −1). The first is better in both columns, so *Fold W, Fold L* is **dominated**.
- Both "Fold with W" rows are gone, so **P1 always bets with W**. (This is slide 58's "B_W¹ = 1".)

**The reduced 2×2 game:**

| Teacher \ Student | call | fold | row min |
|---|---|---|---|
| **Bet W, Bet L** (sometimes bluffs) | 0 | 1 | 0 |
| **Bet W, Fold L** (honest) | ½ | 0 | 0 |
| **column max** | ½ | 1 | |

Max-min = 0 and min-max = ½. They are **not equal, so there is no saddle point and no pure solution**. The true value lies between 0 and ½, and it turns out to be ⅓.

### Slide 54: Finding the solution for tiny poker
**Question:** is there a Nash equilibrium in pure strategies only? **Answer: No!**
1. If Player 1 **always bets**, Player 2 should **always bet** (call). *(Against "Bet W, Bet L": calling gives P1 0, folding gives P1 1. P2 wants P1's payoff low, so P2 calls.)*
2. But if Player 2 always calls, Player 1 should **fold with the losing card**. *(Against call: "Bet W, Fold L" gets ½ > 0.)*
3. But if Player 1 always folds with the losing card, Player 2 should **always fold**. *(Now a bet means P1 must have W, so calling loses 2 while folding loses only 1.)*
4. But if Player 2 always folds, Player 1 should **always bet**. *(Against fold: "Bet W, Bet L" gets 1 > 0. Bluff freely!)*
5. *And round and round it goes.*

💡 **INTUITION:** this is **exactly the same cycling** as matching pennies (slides 9 and 30). Cycling best responses tell you that the equilibrium must be **mixed**.

### Slide 55: Now we play the game
*"(fun, fun, fun)."* An in-class demonstration where the lecturer plays tiny poker against the students.

### Slide 56: What did I do?
- With a **winning card, I always bet**. *(Why?)* **Dominance:** betting with W gives +1 or +2 depending on P2, while folding gives −1. Betting is better **whatever** P2 does.
- With a **losing card, I bet ⅓ of the time.** This is the **bluffing** frequency.
- **You should have bet (called) ⅔ of the time.**

The rest of the section *derives* these numbers.

### Slides 57–58: We seek a mixed strategy for tiny poker
Let:
- **B_W¹** = probability Player 1 bets with the **winning** card;
- **B_L¹** = probability Player 1 bets with the **losing** card (the **bluffing probability**);
- **B²** = probability Player 2 bets (**calls**);
- **U** = payoff to Player 1, so **−U** is the payoff to Player 2.

*What should B_W¹ be?* **B_W¹ = 1, by dominance** (see slide 56).

💡 **INTUITION:** once B_W¹ = 1 is fixed, there are only **two unknowns**: B_L¹ for P1 and B² for P2. Each player effectively has one probability to choose, so the game behaves like a **2×2 game** and the **graphical method** works again. (The "Back to Tiny Poker Trees" button is a link back to the tree on slide 47.)

### Slides 59–64: A graphical solution for player 1
*(Slides 62–64 are an exact repeat of slides 59–61.)*

**Axes:** horizontal = **B_L¹** (how often P1 bluffs). Vertical = **payoff to player 1**.
- **Blue line, "B² = 0"** (P2 always folds): **U = B_L¹**. It rises from (0, 0) to (1, 1). Against someone who never calls, **the more you bluff the better**.
- **Orange line, "B² = 1"** (P2 always calls): **U = ½(1 − B_L¹)**. It falls from (0, 0.5) to (1, 0). Against someone who always calls, **bluffing costs you money**.
- **Thick red line, "minimum"** (slides 60 and 63): the **lower envelope**, i.e. what P1 is **guaranteed** whatever P2 does. It is a **Λ shape** again.
- **Dashed lines** (slides 61 and 64): the peak of the Λ is at **B_L¹ = ⅓, payoff ⅓**.

🧮 **WORKED MATHS:** the lines cross where B_L¹ = ½(1 − B_L¹), so (3/2)·B_L¹ = ½, giving **B_L¹ = ⅓** and **U = ⅓**.

| B_L¹ (bluff prob.) | vs always fold: B_L¹ | vs always call: ½(1 − B_L¹) | P1's worst case = min |
|---|---|---|---|
| 0 | 0 | 0.5 | 0 |
| 1/6 | 0.167 | 0.417 | 0.167 |
| **1/3** | **0.333** | **0.333** | **0.333 ← maximum** |
| 1/2 | 0.5 | 0.25 | 0.25 |
| 1 | 1 | 0 | 0 |

### Slides 65–73: A graphical solution for player 2
*(Slides 65–67 are built up, then repeated as 68–70 and 71–73.)*

**Axes:** horizontal = **B²** (how often P2 calls). Vertical = **payoff to player 1**, which P2 wants to be **low**.
- **Line falling from (0, 1) to (1, 0):** P1 **always bluffs** (B_L¹ = 1). Then **U = 1 − B²**. If P2 never calls, P1 wins every pot. The more P2 calls, the more P1's bluffs get caught.
- **Line rising from (0, 0) to (1, 0.5):** P1 **never bluffs** (B_L¹ = 0). Then **U = B²/2**. P1 only bets with W, so every call by P2 just hands over 2 instead of 1.
- **Thick red line, "maximum":** the **upper envelope**, P2's **worst case**, because P1 picks whichever is better for him. It is a **V shape**.
- **Dashed lines:** the bottom of the V is at **B² = ⅔, payoff ⅓**.

⚠️ **WATCH OUT (slide errors on these graphs):**
1. **The legend labels are swapped.** The slide labels the falling line (from 1 to 0) "B_L¹ = 0" and the rising line (from 0 to 0.5) "B_L¹ = 1". By the algebra on slide 79, the **falling** line is **B_L¹ = 1** (U = 1 − B²) and the **rising** line is **B_L¹ = 0** (U = B²/2). **Sanity check:** if P1 never bluffs and P2 never calls, P1 gets +1 with W and −1 with L, so U = 0. That is the line starting at 0, so the line starting at 0 must be B_L¹ = 0.
2. On slides **66, 69 and 72** the horizontal axis is labelled **B_L¹**, but it should be **B²** (the same graph on slides 67, 70 and 73 correctly says B²).

🧮 **WORKED MATHS:** 1 − B² = B²/2, so (3/2)·B² = 1, giving **B² = ⅔** and **U = ⅓**.

| B² (call prob.) | P1 always bluffs: 1 − B² | P1 never bluffs: B²/2 | P2's worst case = max |
|---|---|---|---|
| 0 | 1 | 0 | 1 |
| 1/3 | 0.667 | 0.167 | 0.667 |
| **2/3** | **0.333** | **0.333** | **0.333 ← minimum** |
| 5/6 | 0.167 | 0.417 | 0.417 |
| 1 | 0 | 0.5 | 0.5 |

⭐ **KEY RESULT:** P1's max-min = ⅓ = P2's min-max, so **the value of tiny poker is ⅓**. On average **Player 1 wins £⅓ per game**, and Player 2 cannot prevent it.

### Slides 74–75: Player 1's mixed strategies against Player 2's pure strategies (the algebra)
On the slide, the **magenta** terms come from the **W card** and the **blue** terms come from the **L card**. The ½ in front is the probability of each card.

🧮 **WORKED MATHS: Player 2 always calls (B² = 1):**

```
U(B_L¹, B²=1) = ½ [ 2  +  (−2)·B_L¹ + (−1)·(1 − B_L¹) ]
                    └W┘   └────────── L card ──────────┘
              = ½ [ 2 − 2B_L¹ − 1 + B_L¹ ]
              = ½ (1 − B_L¹)
```

- **W:** P1 bets (B_W¹ = 1) and P2 calls, so **+2**.
- **L:** P1 bluffs with probability B_L¹, gets called, and loses **−2**. With probability 1 − B_L¹ he folds and loses **−1**.

🧮 **WORKED MATHS: Player 2 always folds (B² = 0):**

```
U(B_L¹, B²=0) = ½ [ 1  +  (1)·B_L¹ + (−1)·(1 − B_L¹) ]
              = ½ [ 1 + B_L¹ − 1 + B_L¹ ]
              = ½ · 2B_L¹
              = B_L¹
```

- **W:** P1 bets and P2 folds, so **+1**.
- **L:** a bluff makes P2 fold, so **+1** with probability B_L¹. Otherwise P1 folds, **−1**.

These two results are exactly the two lines on the player-1 graph (slides 59–64).

### Slides 76–78: Solution (for player 1)
- Solve **U(B_L¹, B² = 1) = U(B_L¹, B² = 0)**.
- **Why?** *Otherwise Player 2 would have a best pure strategy.* If calling were better for P2, P2 would always call. If folding were better, P2 would always fold. Either way P1 gets exploited (this is the indifference principle again).
- *It can be viewed as a **max-min solution*** (it is the peak of the red Λ).
- *"We can solve for **B_L¹ = ⅓**. So, **bluff one third of the time** for an expected payoff of **⅓ per game**."*

🧮 ½(1 − B_L¹) = B_L¹, so 1 − B_L¹ = 2B_L¹, giving **B_L¹ = ⅓**. The payoff is U = ⅓.

### Slide 79: Player 2's mixed strategies against Player 1's pure strategies
*Assume Player 2 knows that B_W¹ is 1.*

🧮 **WORKED MATHS: Player 1 always bets with the losing card (B_L¹ = 1):**

```
U(B_L¹=1, B²) = ½ [ (2)·B² + (1)·(1 − B²)  +  (−2)·B² + (1)·(1 − B²) ]
                    └─────── W card ──────┘   └─────── L card ───────┘
              = ½ [ 2B² + 1 − B² − 2B² + 1 − B² ]
              = ½ [ 2 − 2B² ]
              = 1 − B²
```

- **W:** P2 calls, giving +2. P2 folds, giving +1.
- **L (bluff):** P2 calls, giving −2. P2 folds, giving +1.

🧮 **WORKED MATHS: Player 1 always folds with the losing card (B_L¹ = 0):**

```
U(B_L¹=0, B²) = ½ [ (2)·B² + (1)·(1 − B²)  − 1 ]
              = ½ [ 2B² + 1 − B² − 1 ]
              = B² / 2
```

- **W:** the same as before. **L:** P1 folds and loses 1, whatever P2 does.

**Set them equal:** 1 − B² = B²/2, so **B² = ⅔**, and the payoff **to Player 2 is −⅓**.

💡 **INTUITION: what the poker result means**
- **Why bluff at all?** If P1 *never* bluffs, a bet **reveals** that he holds W, so P2 always folds. P1 then wins +1 with W and loses 1 with L, an average of **0**. Bluffing ⅓ of the time raises his average to **⅓**. **Bluffing is not a trick or a psychological gamble. It is the mathematically optimal strategy.**
- **Why not bluff more?** If P1 bluffs too much, P2 should call every time, and each bluff then loses 2.
- **Why call exactly ⅔?** If P2 calls *less*, bluffing becomes profitable and P1 would bluff every time. If P2 calls *more*, P1 should stop bluffing, and then every call just pays out 2 to a W hand.
- **Who has the edge?** P1, with value +⅓. His advantage is **information**: he sees the card.

➕ **BEYOND THE SLIDES: a Bayesian check of P2's indifference.** At equilibrium, P1 bets with W always and with L ⅓ of the time. So, given that P1 bet:

```
P(W | bet) = (½ · 1) / (½ · 1 + ½ · ⅓) = (½) / (⅔) = ¾
P2 calls:  ¾ · (−2) + ¼ · (+2) = −1
P2 folds:  −1   (loses the ante)
```

Calling and folding are worth **exactly the same** to P2 (−1 each). The bluffing rate of ⅓ is precisely the rate that makes P2's decision a coin-toss in value, which is the indifference principle seen from P2's side.

### Slide 80: Conclusions (on the poker section)
1. **There exists a mini-max equilibrium for all two-player games with perfect information, even with chance.** *(Backward induction, or expectiminimax when there are chance nodes, always works and gives pure strategies.)*
2. **With imperfect information, we have to allow for mixed strategies.** *(As in tiny poker: P2's information set makes pure strategies cycle.)*
3. **All finite games have at least one Nash equilibrium.** *(Nash's theorem, slide 14.)*

---

# Part 6: Example 3, generalised Rock-Paper-Scissors (Slides 81–97)

### Slides 81–82: Ordinary Rock-Paper-Scissors

Payoffs to Player 1:

| P1 \ P2 | Rock | Paper | Scissors |
|---|---|---|---|
| **Rock** | 0 | −1 | 1 |
| **Paper** | 1 | 0 | −1 |
| **Scissors** | −1 | 1 | 0 |

**Solution: (⅓, ⅓, ⅓)** for both players. The value is 0.

🧮 **Check with the indifference principle.** If P2 plays uniformly:
- U(Rock) = ⅓(0) + ⅓(−1) + ⅓(1) = **0**
- U(Paper) = ⅓(1) + ⅓(0) + ⅓(−1) = **0**
- U(Scissors) = ⅓(−1) + ⅓(1) + ⅓(0) = **0**

All three are equal, so P1 is indifferent. By symmetry the same holds for P2, so this is a Nash equilibrium ✓.

### Slide 83: The modified game
Now **Rock beats Scissors by 1000** (shown in red on the slide): the Rock-vs-Scissors cell is **+1000**, and the Scissors-vs-Rock cell is **−1000**.

| P1 \ P2 | Rock | Paper | Scissors |
|---|---|---|---|
| **Rock** | 0 | −1 | **1000** |
| **Paper** | 1 | 0 | −1 |
| **Scissors** | **−1000** | 1 | 0 |

*Solution: ?, ?, ?*

### Slide 84: Questions
**Q1. Could the Nash equilibrium consist of pure strategies?** **No.**
- Row minima: Rock −1, Paper −1, Scissors −1000, so max-min = **−1**.
- Column maxima: Rock column 1, Paper column 1, Scissors column 1000, so min-max = **+1**.
- −1 ≠ +1, so there is **no saddle point**.
- Put simply: whatever pure strategy the opponent plays, you can switch to the one that beats it. The best responses cycle (Rock → Paper → Scissors → Rock).

**Q2. Is (⅓, ⅓, ⅓) still a Nash equilibrium?** **No.** If P2 plays uniformly, P1's payoffs are:
- U(Rock) = ⅓(0 − 1 + 1000) = **333**
- U(Paper) = ⅓(1 + 0 − 1) = **0**
- U(Scissors) = ⅓(−1000 + 1 + 0) = **−333**

These are **not equal**. P1's best response is **pure Rock** (333 > 0), so P1 would deviate and the uniform profile is **not** an equilibrium.

**Q3. Why or why not?** Because the payoffs are no longer balanced, the uniform mix no longer makes the opponent **indifferent**, and the indifference principle fails.

### Slide 85: Strategies
**Player 1:**
- **x_R**, the probability of playing Rock;
- **x_P**, the probability of playing Paper;
- **x_S**, the probability of playing Scissors.
- Obviously **x_R + x_P + x_S = 1**.

**Player 2:** likewise with **y_R, y_P, y_S**.

### Slides 86–89: Payoff to player 1
Each formula is **one row of the matrix, weighted by P2's probabilities**:

```
U⁽¹⁾(R) =     0·y_R + (−1)·y_P + 1000·y_S   =  [ −y_P + 1000·y_S ]
U⁽¹⁾(P) =     1·y_R +    0·y_P + (−1)·y_S   =  [ y_R − y_S ]
U⁽¹⁾(S) = −1000·y_R +    1·y_P +    0·y_S   =  [ −1000·y_R + y_P ]
```

U⁽¹⁾(R) means P1's expected payoff if P1 plays Rock and P2 plays the mix (y_R, y_P, y_S).

### Slides 90–95: Make the terms in square brackets the same. Why?
- **Slide 90:** *To make a Nash equilibrium, make the terms in square brackets the same.*
- **Slides 91–93: Why?** *Because, if otherwise, the biggest one would be the best response, and thereby would constitute a pure Nash equilibrium strategy.*
- **Slide 94: Thus** U⁽¹⁾(R) = U⁽¹⁾(P) = U⁽¹⁾(S) = **K** (one common number).
- **Slide 95:** so **U⁽¹⁾ = K**. *Whatever mix P1 uses*, P1 gets K, because an average of equal numbers is that number (the same argument as slides 27–29).
- *"So Player 2 also wants to make K as small as possible."* K is what P1 wins, which is exactly what P2 loses. *"Any thoughts on the value of K?"*

⚠️ **WATCH OUT (precise version of the "Why?"):** the slide's wording is a little loose. Here is the careful argument.
- If one bracket were **strictly largest**, P1's **unique** best response would be that **pure** strategy, so P1 would put all his probability on it.
- But Q1 showed there is **no pure equilibrium**. So in equilibrium P1 cannot be playing pure, and hence the brackets for the strategies P1 actually uses must **tie**.
- **General rule:** *every pure strategy played with positive probability in a Nash equilibrium must earn the same, maximal, expected payoff. Strategies played with probability 0 may earn **less than or equal to** K.* Here all three strategies are used, so all three brackets equal K.

### Slide 96: Solving
We need to solve the system of linear equations:

```
[ −y_P + 1000·y_S ]   = K
[ y_R − y_S ]         = K
[ −1000·y_R + y_P ]   = K

with   y_R + y_P + y_S = 1        (5)
       y_R ≥ 0                    (6)
       y_P ≥ 0                    (7)
       y_S ≥ 0                    (8)
                                  (9)  ← empty; just a typesetting leftover
```

*"…which can only be solved if K = 0."*

🧮 **WORKED MATHS: why K must be 0** (the slide states this without proof):
- From equation 2: **y_R = y_S + K**.
- From equation 1: **y_P = 1000·y_S − K**.
- Substitute both into equation 3: −1000(y_S + K) + (1000·y_S − K) = K. This simplifies to −1000K − K = K, so **−1002·K = 0**, giving **K = 0**.

💡 **INTUITION: why K = 0 without any algebra:** the game is **symmetric**. Both players have the same options, and the matrix is **skew-symmetric** (Aᵀ = −A, i.e. swapping the players just flips the sign). A symmetric zero-sum game is **fair**. If P1 could guarantee K > 0, then P2 could use the **same** strategy and guarantee the same against P1, which contradicts K > 0. So the value must be 0.

### Slide 97: Solution
With K = 0:
- Equation 2 gives **y_R = y_S**.
- Equation 1 gives **y_P = 1000·y_S**.
- Equation 3 gives y_P = 1000·y_R, which is consistent with the first two.
- Normalise using (5): y_R + 1000·y_R + y_R = 1, so **1002·y_R = 1**.

```
y_R = 1/1002    ≈ 0.000998
y_P = 1000/1002 ≈ 0.998
y_S = 1/1002    ≈ 0.000998
```

*"By symmetry, x_R, x_P, x_S are likewise. So, **almost always play paper**."*

🧮 **Check that P1's mix makes P2 indifferent** (payoff to P1 for each pure choice of P2, using the x's above):
- P2 plays Rock: 0·x_R + 1·x_P + (−1000)·x_S = (1000 − 1000)/1002 = **0**
- P2 plays Paper: (−1)·x_R + 0·x_P + 1·x_S = (−1 + 1)/1002 = **0**
- P2 plays Scissors: 1000·x_R + (−1)·x_P + 0·x_S = (1000 − 1000)/1002 = **0**

All equal ✓.

💡 **INTUITION: why mostly *Paper*, when the big prize is on Rock vs Scissors?** This is counter-intuitive, and a favourite exam trap.
- For **Scissors** to be worth playing (equal to the others), it wins only +1 against Paper but loses 1000 against Rock. So the opponent's Rock must be **1000 times rarer** than their Paper: **y_P = 1000·y_R**.
- For **Rock** not to be *too* attractive, its +1000 against Scissors must be balanced by its −1 against Paper. So the opponent's Scissors must be **1000 times rarer** than their Paper: **y_P = 1000·y_S**.
- So **both Rock and Scissors become rare**, and Paper takes almost all the probability.
- **Lesson: a huge payoff on a match-up does not make you play the winning strategy more. It makes the strategies involved in that match-up *rarer*.** Your probabilities are set by your **opponent's** payoffs (the indifference principle), not by your own temptations.
- **Typical outcome:** both players play Paper with probability ≈ 0.998² ≈ **0.996**, so the game is almost always a draw.

➕ **BEYOND THE SLIDES: generalise.** Replace 1000 with any M > 0. The same algebra gives **y_R = y_S = 1/(M + 2)** and **y_P = M/(M + 2)**. With M = 1 this is (⅓, ⅓, ⅓), the ordinary game ✓. With M = 1000 it is the slide's answer ✓.

---

# Part 7: Conclusions (Slide 98)

### Slide 98: Conclusions on mixed strategies
- **Mixed strategies** are probabilistic mixtures of pure strategies.
- Once mixed strategies are allowed, **equilibria exist in all finite games** (Nash).
- For **two-player, zero-sum** games, finding equilibria is a **linear problem** (linear programming, slide 15).
- Mixed strategies are often required **to prevent opponents from predicting your actions**.

---

# Errata: mistakes and inconsistencies on the slides

| # | Slide(s) | What the slide says | What it should say |
|---|---|---|---|
| 1 | 25–26 | Task: Ex[U₂(**S₂**(x), Red)] = … | Ex[U₂(**S₁**(x), Red)], because x is Donald's (P1's) probability |
| 2 | 30 | "payoff **to Donald** is bigger…", written with **U₂** | Use **U₁** (Donald's payoff), or keep U₂ and flip the inequality |
| 3 | 65–73 | Legend: falling line = "B_L¹ = 0", rising line = "B_L¹ = 1" | **Swapped:** falling line (1 − B²) is **B_L¹ = 1**, rising line (B²/2) is **B_L¹ = 0** (compare slide 79) |
| 4 | 66, 69, 72 | Horizontal axis labelled **B_L¹** | Should be **B²** (as on slides 67, 70, 73) |
| 5 | 44 | "its component of the of the *mixed*…" | "its component of the *mixed*…" |
| 6 | 96 | Equation number (9) with no equation | Typesetting leftover; ignore it |

None of these change any of the final answers.

---

# Cheat sheet

| Concept | One-line summary |
|---|---|
| Best response | Your best strategy, holding the others fixed |
| Nash equilibrium | A **profile** where everyone is best-responding, so there is no profitable *unilateral* deviation |
| Max-min / min-max | P1 maximises the worst case; P2 minimises P1's best case. Equal means saddle point and the value of the game |
| Mixed strategy | A probability distribution over pure strategies (qᵢ ≥ 0, Σqᵢ = 1) |
| Extensive-form mixing | Probabilities at each **information set**, the same at every node inside it |
| When needed | Hidden information: poker, or any simultaneous-move (normal-form) game |
| Nash's theorem | Every finite game has ≥ 1 Nash equilibrium (possibly mixed) |
| Algorithms | General-sum: Lemke–Howson (can be exponential). Zero-sum: linear programming |
| **Indifference principle** | Mix so that the **opponent** gets equal payoffs from every pure strategy they use |
| Why it works | Opponent indifferent, so every reply is a best response, so there is no incentive to deviate |
| Graphical 2×2 | Plot one line per opponent pure strategy. Maximiser takes the **top of the lower envelope (Λ)**; minimiser takes the **bottom of the upper envelope (V)** |
| Brothers / matching pennies | x = y = ½, value 0 |
| Tiny poker | Always bet with W, bluff with L ⅓ of the time, call ⅔ of the time, value **+⅓** to P1 |
| RPS | (⅓, ⅓, ⅓), value 0 |
| RPS with 1000 | (1/1002, 1000/1002, 1/1002), value 0: "almost always play Paper" |
| 2×2 formula ➕ | D = a − b − c + d, x* = (d − c)/D, y* = (d − b)/D, value = (ad − bc)/D |

---

# Self-test questions (answers below)

1. State the indifference principle. Whose payoffs determine **your** mixing probabilities?
2. Show that matching pennies has no pure-strategy Nash equilibrium, using max-min and min-max.
3. Zero-sum game, payoffs to Row: `[[3, −1], [−2, 1]]`. Find both players' equilibrium mixed strategies and the value.
4. In tiny poker, why is B_W¹ = 1?
5. In tiny poker, suppose Player 2 calls with probability ½ instead of ⅔. What should Player 1 do, and what does he earn?
6. In the 1000-RPS game, is (⅓, ⅓, ⅓) a Nash equilibrium? Justify numerically.
7. True or false: "At a mixed Nash equilibrium a player is indifferent between their pure strategies, so it doesn't matter what mix they play."
8. Why does the generalised RPS have value K = 0?

### Answers
1. **Each player chooses their mix so that the *opponent* is indifferent between the opponent's pure strategies.** Your probabilities are determined by your **opponent's** payoffs.
2. Row minima are −1 and −1, so max-min = −1. Column maxima are 1 and 1, so min-max = 1. Since −1 ≠ 1 there is no saddle point. Checking all four cells, someone always gains by switching, so there is no pure Nash equilibrium.
3. Row minima are −1 and −2 (max-min −1), and column maxima are 3 and 1 (min-max 1), so there is no saddle point. D = 3 − (−1) − (−2) + 1 = 7. **x\* = (1 − (−2))/7 = 3/7** (Row plays row 1). **y\* = (1 − (−1))/7 = 2/7** (Column plays column 1). **Value = (3·1 − (−1)(−2))/7 = 1/7.**
   Check: 3·(3/7) − 2·(4/7) = 1/7 and −1·(3/7) + 1·(4/7) = 1/7 ✓.
4. **Dominance.** With W, betting earns +1 (P2 folds) or +2 (P2 calls), while folding earns −1. Betting is strictly better whatever P2 does.
5. With B² = ½: always bluffing gives U = 1 − ½ = **½**, never bluffing gives U = ½/2 = ¼. So P1 should **always bluff** (B_L¹ = 1) and earns **½ > ⅓**. Player 2 is being exploited, which is why P2 must call exactly ⅔ of the time.
6. **No.** Against a uniform P2: U(R) = 999/3 = 333, U(P) = 0, U(S) = −999/3 = −333. These are not equal, so P1 deviates to pure Rock.
7. **False** (in the sense that matters). Against the opponent's equilibrium strategy, every mix earns the same. But if you change your mix, the opponent is **no longer indifferent**, gets a strictly better pure reply, and exploits you (slide 44).
8. Algebraically, substituting the three equations into each other gives −1002K = 0. Intuitively, the game is symmetric and zero-sum (Aᵀ = −A). If P1 could guarantee K > 0, P2 could copy that strategy and guarantee K > 0 for himself, which is impossible. So K = 0.
