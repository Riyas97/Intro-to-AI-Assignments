# Intro-to-AI-Assignments

## Summary
This repo comprises of the assignments that I did which are related to artificial intelligence. This repo can be split into two parts, namely Pacman and Sudoku.

## Part 1: Pacman
For this part, several search algorithms and heuristics were implemented as part of the Pacman game. 
Using them, the Pacman agent will find paths through his maze world, both to reach a particular location and
to collect food efficiently. The tasks were:

- Implement depth-first graph search (DFS) algorithm to find a fixed food dot in the maze.
- Implement breadth-first graph search (BFS) algorithm to find a fixed food dot in the maze.
- Implement uniform-cost graph search (UCS) algorithm to find a fixed food dot in the maze.
- Implement A∗ graph search algorithm to find a fixed food dot in the maze.
- Formulate a search problem to find the shortest path through the maze that touches all four corners (CornersProblem).
- Implement a non-trivial, consistent heuristic for the CornersProblem.
- Implement a Q-learning agent as well as an approximate Q-learning agent and train them to play the game of Pacman

Before you run the programs, ensure you are using Python 2.7.

To run, first proceed to `/Pacman/Code`. Then, 

- to run the DFS algorithm, run `python pacman.py -l bigMaze -z .5 -p SearchAgent`
- to run the BFS algoithm, run `python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5`
- to run the UCS algorithm, run `python pacman.py -l mediumScaryMaze -p StayWestSearchAgent`
- to run the A∗ graph search algorithm, run `python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`
- to run the corners problem, run `python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem` 
and/or run `python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5`

## Part 2: Sudoku
For this part, the task was to design an efficient Sudoku solver either by using local search technique (such as hill climbing,
variants of simulated annealing) or use constraints followed by backtracking search and inference.

Before you run the programs, ensure you are using Python 2.7.

To run, first proceed to `/Sudoku/Code`. Then, 

- run `python CS3243_P2_Sudoku_00.py input/input_1.txt output.txt`
