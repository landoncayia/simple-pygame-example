# Simple Pygame Example

This is a simple example of a game built with the Pygame module, meant for CS205 students at the University of Vermont.

## Gameplay

This game has the following components:
* A **board**, which is the outer squares of a 9x9 grid.
* Blue and red **pieces**, which belong to the player and computer, respectively.
* A virtual **six-sided die**, which is used by the player and computer to determine the number of squares he or she may move.

The game progresses like this:
1. Start with two of each piece color on the board.
2. The player (blue) rolls using the 'Roll' button. The player may move either piece as many squares as the die roll allows, so long as it follows the principles outlined in the "*Rules & Mechanics*" section.
3. The computer (red) rolls and moves, capturing if possible.
4. (2) and (3) will repeat until either the player or computer have no pieces left - game over!
5. The player may then close the window and launch `main.py` again to start a new game.

## Rules & Mechanics
* Two of the same color piece may not occupy a single square.
* When either the player or computer completely runs out of pieces, the game is over.
* The player may choose not to capture a piece even if it is possible, but the computer will always capture if it can!

## References

Dice icons made by delapouite