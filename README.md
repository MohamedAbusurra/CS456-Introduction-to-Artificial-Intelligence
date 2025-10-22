-- CS456 INTRODUCTION-TO-ARTIFICIAL-INTELLIGENCE

This repository contains two Python programs that solve the classic 8-tile puzzle for CS456 Assignments 1 and Python and Java code for assignment2.

The first performs uninformed search algorithms, and the second implements informed search algorithms with heuristics.

— CS456 – Assignment 1: Eight-Tile Puzzle (Uninformed Search)

This program solves the 8-tile puzzle using uninformed search algorithms as required in Assignment 1.

— Implemented Algorithms

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening Search (IDS)

— Description
The program finds a sequence of moves from the start state to the goal state for the eight-tile puzzle using the selected search method.
It displays:

- The sequence of board configurations from start state to goal state
- The order of actions from the start state to the goal state (Up, Down, Left, Right)
- Solution cost (total number of moves to reach the goal state)
- Number of nodes generated and expanded during search execution
- Total search time for each algorithm

— CS456 – Assignment 2: Eight-Tile Puzzle (Heuristic Search)

This program solves the 8-tile puzzle using informed search algorithms as required in Assignment 2.

— Implemented Algorithms

- Greedy Best-First Search (GFS)
- A\* Search

— Heuristic Functions

- H1: Counts the number of tiles not in their correct position.
- H2: Counts the number of tiles not in their correct row plus number of tiles not in their correct column .

— Description
The program finds a sequence of moves from the start state to the goal state using the selected informed search method and heuristic.
It displays:

- The sequence of board configurations from start state to goal state
- The order of actions from the start state to the goal state (Up, Down, Left, Right)
- Solution cost (total number of moves to reach the goal)
- Number of nodes generated and expanded during search execution
- Total search time for each algorithm
