apply By backward reasoning, one can recursively evaluate a non-final position as identical to the position that is one move away and best valued for the player whose move it is.

---

This describes the fundamental principle of **minimax evaluation** in game theory and artificial intelligence.

In backward reasoning (also called backward induction), you evaluate a position by looking ahead to all possible moves and their resulting positions. The key insight is that a non-terminal position's value equals the value of the best position that can be reached in one move by the current player.

Here's how it works recursively:

**For a maximizing player:** The position's value equals the maximum value among all positions reachable in one move.

**For a minimizing player:** The position's value equals the minimum value among all positions reachable in one move.

**The recursive structure:**

```
evaluate(position) = 
  if position is terminal:
    return terminal_value(position)
  else if current_player is maximizing:
    return max(evaluate(child) for child in children(position))
  else:
    return min(evaluate(child) for child in children(position))
```

This creates a recursive evaluation tree where:

- Leaf nodes have known values (win/loss/draw)
- Internal nodes inherit their value from their best child
- The "best" child alternates between maximum and minimum depending on whose turn it is

This principle underlies many game-playing algorithms, from simple tic-tac-toe solvers to sophisticated chess engines. The backward reasoning ensures that each player plays optimally, assuming their opponent will also play optimally.