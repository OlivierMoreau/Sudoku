# Sudoku 

## A pygame 

Includes so far the following functionalities :

- An auto solver

- Checking your inputs

- Hints 

- Levels of difficulty

- An auto save/load system

- 3k grids

How the game works :

- sudoku.py is the initial file used to instantiate the engine of the game and values such as screen size.

- engine.py is the main engine of the game with a loop running around 60 times a second. This class includes methods to react to user inputs and to update the screen.
it is also responsible of the saving/loading system as well as the UI. The engine also manages a Game and Grid object.

- game.py is the instance of the current game. contains methods regarding the currect game such as checking user inputs and so on.

- grid.py is the sudoku grid itself. It is composed of Block objects (rows etc) and Cell objects and manages methods such as the auto-solve.

**Auto solving function :**
The auto solving function is a recursive function that solves the grid by brute forcing every single possible inputs.

In every cell we try every inputs until we find a legal move, then proceeds to the next cell by calling itself again.

When the auto solver reaches a dead end (tried every digits in a cell without finding a legal move) it back tracks to the previous function call, and tries again until it reachs a completed grid.

**Saving system:**
The saving system uses "pickle" a module allowing to serialize objects states in binary files. This happens when pygame detects a shutdown even, as well as once a minute.

This file is then read at the initialization of the program, and the relevant data is loaded into the game by the engine.

**Hints cheat:**
To save time the program knows what the correct value of each cell is so it doesn't have to solve it everytime the user requests a hint.


####*Author: Olivier Moreau*

####*olivier.moreau0@laposte.net*




