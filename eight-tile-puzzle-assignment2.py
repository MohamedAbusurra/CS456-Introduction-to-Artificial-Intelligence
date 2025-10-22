import time
import heapq

class TilePuzzle:
    def __init__(self, tile_board):
        # Initializes the puzzle board and stores its size.
        # Keeps a copy of the original input state in case it is altered elsewhere in the program.
        # The size n of the board is recorded for boundary checks.
        self.board = [row[:] for row in tile_board]
        self.n = len(tile_board)

    def find_blank(self, state):
        # Locates the position of the blank (0) in the puzzle.
        # Traverses the 2D list and returns the coordinates of the blank (0) when found.
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:
                    return i, j
        return None  # Added for safety; in a valid puzzle there should always be exactly one blank.

    def copy_and_swap(self, state, x1, y1, x2, y2):
        # Creates a copy of the board so swapping does not alter the original state.
        # Swaps the two tiles at the given coordinates and returns the new board state.
        successor = [row[:] for row in state]
        successor[x1][y1], successor[x2][y2] = successor[x2][y2], successor[x1][y1]
        return successor
    
    def calculate_h1(self, successor, goal_state):
        heuristic_one = 0
        # Traverse the generated tiles row by row.
        # Ignore zero which is the empty tile.
        # Check each value against the goal state at the same position.
        # If the values do not match (and the tile is not 0), increment the heuristic by one.
        for i in range(len(successor)):
            for j in range(len(successor[i])):
                if successor[i][j] != goal_state[i][j] and successor[i][j] != 0:
                    heuristic_one += 1
        return heuristic_one
    
    def calculate_h2(self, successor, goal_state):
        heuristic_two = 0
        # Traverse the grid row by row (row-major order).
        # Ignore zero, which is the empty tile.
        # For each row, get the corresponding row from the goal_state.
        # For each tile, check if its value appears anywhere in that goal row (ignoring 0).
        # If it is not present, increment the heuristic.
        for i in range(len(successor)):
            goal_row = goal_state[i]
            for j in range(len(successor[i])):
                if successor[i][j] not in goal_row and successor[i][j] != 0:
                    heuristic_two += 1

        # Traverse the grid column by column (column-major order).
        # Ignore zero, which is the empty tile.
        # For each column, build the list of values from that column in the goal_state.
        # For each tile, check if its value appears anywhere in that goal column (ignoring 0).
        # If it is not present, increment the heuristic.
        for j in range(len(successor[0])):
            goal_col = [row[j] for row in goal_state]
            for i in range(len(successor)):
                if successor[i][j] not in goal_col and successor[i][j] != 0:
                    heuristic_two += 1
        return heuristic_two
    
    def to_tuple(self, state):
        # Converts the board state to an immutable tuple form to allow for use in sets.
        # Used to keep track of explored states to prevent re-exploring the same state in a search.
        return tuple(tuple(row) for row in state)

    def move_up(self, state):
        # Moves the blank tile up if possible.
        # Checks that the blank tile is not on the top row (x > 0) before swapping.
        x, y = self.find_blank(state)
        if x > 0:
            return self.copy_and_swap(state, x, y, x - 1, y), "Up"
        return None, None

    def move_down(self, state):
        # Moves the blank tile down if possible.
        # Checks that the blank tile is not on the bottom row (x < self.n - 1) before swapping.
        x, y = self.find_blank(state)
        if x < self.n - 1:
            return self.copy_and_swap(state, x, y, x + 1, y), "Down"
        return None, None

    def move_left(self, state):
        # Moves the blank tile left if possible.
        # Checks that the blank tile is not in the leftmost column (y > 0) before swapping.
        x, y = self.find_blank(state)
        if y > 0:
            return self.copy_and_swap(state, x, y, x, y - 1), "Left"
        return None, None

    def move_right(self, state):
        # Moves the blank tile right if possible.
        # Checks that the blank tile is not in the rightmost column (y < self.n - 1) before swapping.
        x, y = self.find_blank(state)
        if y < self.n - 1:
            return self.copy_and_swap(state, x, y, x, y + 1), "Right"
        return None, None

    def expand_node(self, state):
        # Expands the current state into all possible successor states.
        # Creates a list to store valid next states and their corresponding actions.
        # Defines a list called 'operator' containing the move functions to generate expanded states.
        # Iterates through the operators, returning the new_state and action if move possible.
        # Unpacks and stores each successor and action.
        # Returns the list of possible moves.
        successors = []
        # Creates a list of all possible next action functions.
        # Calls action functions with the state passed as a parameter.
        # Only add results that are not None (i.e., legal moves).
        for operator in [self.move_up, self.move_down, self.move_left, self.move_right]:
            successor, action = operator(state)
            if successor is not None:
                successors.append((successor, action))
        return successors

    def reconstruct(self, state):
        # Reconstructs the path and actions from the start to the goal.
        # Starts from the provided goal node and follows parent links back to the start.
        # Initializes two lists. "states" which stores each board configuration, and "actions" stores the move that led to it.
        # Traverses from goal back to start using the parent links, storing states and actions.
        # Once the start is reached, reverse both lists to get start to goal order.
        # The start state has no action, so it is skipped in the returned actions.
        states, actions = [], []
        explore = state
        while explore is not None:
            states.append(explore["state"])
            actions.append(explore["action"])
            explore = explore["parent"]
        states.reverse()
        actions.reverse()
        return states, actions[1:]  # Skips the initial None action from root

    def greedy_best_first_search(self, start, goal, heuristic):
        # Implements the Greedy Best-First Search (GBFS) algorithm using a priority queue (heapq).
        # GBFS expands the node that appears closest to the goal based on the heuristic value only.
        root = {"state": start, "parent": None, "action": None}

        # Create an empty list to act as the frontier (priority queue)
        # The counter is used as a tie breaker for equal priorities to prevent dict being used as a tie breaker 
        frontier = []
        counter = 0

        # Condition so the heuristic chosen during the input is called during the search
        if heuristic == "1":
            heapq.heappush(frontier, (self.calculate_h1(start, goal), counter, root))
        else:
            heapq.heappush(frontier, (self.calculate_h2(start, goal), counter, root))
        
        # Initializes a set to keep track of explored states and stores them in a set
        closed = set()  
        #nodes_generated and nodes_expanded initialized to keep track of number of nodes expanded and generated
        nodes_entered_frontier = 1
        nodes_expanded = 0

        # Searches until frontier is empty or goal is found
        while frontier:
            # Removes the node from the frontier with the lowest heuristic value
            _, _, node = heapq.heappop(frontier)
            state = node["state"]
            key = self.to_tuple(state)

            # Skips if already processed
            if key in closed:
                continue
            closed.add(key)
            
            # Checks to see if current state is the goal state
            # if goal state, construct path and actions and return solution
            if state == goal:
                path, actions = self.reconstruct(node)
                return path, actions, nodes_entered_frontier, nodes_expanded
            
            nodes_expanded += 1

            # Expand successors
            for successor, action in self.expand_node(state):
                sucessor_key = self.to_tuple(successor)
                if sucessor_key in closed:
                    continue
                counter += 1
                new_node = {"state": successor, "parent": node, "action": action}
                if heuristic == "1":
                    priority = self.calculate_h1(successor, goal)
                else:
                    priority = self.calculate_h2(successor, goal)
                # pushes new node to the frontier with priority, counter (to resolve tie breaks)
                heapq.heappush(frontier, (priority, counter, new_node))
                nodes_entered_frontier += 1

        # If frontier becomes empty without returning a solutoin, It returns none as no solution exists
        return None, None, nodes_entered_frontier, nodes_expanded

    def a_star_search(self, start, goal, heuristic):
        # Implements the A* Search algorithm using a priority queue (heap).
        # Combines sum of path cost and heuristic to choose the next node to explore.
        root = {"state": start, "parent": None, "action": None, "cumulative_cost": 0}
        frontier = []
        counter = 0

        # Calculate initial heuristic for the starting state.
        if heuristic == "1":
            h0 = self.calculate_h1(start, goal)
        else:
            h0 = self.calculate_h2(start, goal)
        heapq.heappush(frontier, (h0, counter, root))

        # stores the lowest cost to reach each state to compare later on to see if new path to an already discovered node should be added or discarded
        g_lowest = {self.to_tuple(start): 0}  
        # Tracks closed node states
        closed = set()  
        nodes_entered_frontier = 1
        nodes_expanded = 0

        # Search loop
        while frontier:
            # Remove node with the lowest f = g + h value
            _, _, node = heapq.heappop(frontier)
            state = node["state"]
            key = self.to_tuple(state)
            g = node["cumulative_cost"]

            # Skip if already processed at best cost
            if key in closed:
                continue
            closed.add(key)

            # Check if goal reached
            if state == goal:
                path, actions = self.reconstruct(node)
                return path, actions, nodes_entered_frontier, nodes_expanded
             
             #Makes sure the node is not goal state or in closed set before expanding
            nodes_expanded += 1

            # Expand successors
            for successor, action in self.expand_node(state):
                sucessor_key = self.to_tuple(successor)
                # Uniform step cost of one for all successors
                successor_cumulative_cost = g + 1  

                # Only push if this path is cheaper than any path seen before
                if successor_cumulative_cost < g_lowest.get(sucessor_key, float("inf")):
                    g_lowest[sucessor_key] = successor_cumulative_cost
                    counter += 1
                    if heuristic == "1":
                        h = self.calculate_h1(successor, goal)
                    else:
                        h = self.calculate_h2(successor, goal)
                    priority = successor_cumulative_cost + h
                    new_node = {"state": successor, "parent": node, "action": action, "cumulative_cost": successor_cumulative_cost}
                    heapq.heappush(frontier, (priority, counter, new_node))
                    nodes_entered_frontier += 1

        # No solution found
        return None, None, nodes_entered_frontier, nodes_expanded


def reshape(list_one, n):
    # Converts a 1D list into a nxn list (matrix) representation of the puzzle.
    # Takes 'n' elements per row to build an n x n grid.
    board = []
    index = 0
    for _ in range(n):
        board.append(list_one[index:index + n])
        index += n
    return board


def display_result(path, actions, entered_frontier, expanded, print_steps=True):
    # Displays the solution path, actions taken, and search statistics.
    # If no path is found, prints an appropriate message.
    # If path is found, prints each state step-by-step and the associated action list.
    if path is None:
        print("No solution found.\n")
        return
    if print_steps:
        for step, state in enumerate(path):
            print(f"Step {step}:")
            for row in state:
                print(row)
            print()
        print("Actions:", actions)
    print("Solution Cost:", len(actions), "moves")
    print("Nodes Entering Frontier:", entered_frontier)
    print("Nodes Expanded:", expanded)


if __name__ == "__main__":
    matrix_size = 3

    # The start_state is read from "input.txt" in the same folder as the code.
    # Program written and tested on macOS (reading input files on other OS may or may not work).
    with open('input.txt', 'r') as file:
        start_state = [int(number) for line in file for number in line.split()]

    # Manual entry for start state (for quick testing).
    #start_state = [8,7,6,0,4,1,2,5,3] 
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print(start_state)

    # Reshape the start and goal states into 3x3 matrices
    start_state_2d_form = reshape(start_state, matrix_size)
    goal_state_2d_form = reshape(goal_state, matrix_size)

    # Initialize the TilePuzzle object
    puzzle = TilePuzzle(start_state_2d_form)

    # User menu for algorithm and heuristic selection
    while True:
        print("\nSelect the algorithm to solve the Puzzle:")
        print("1. Greedy-Best First Search")
        print("2. A* Search")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "3":
            break

        print("\nSelect the heuristic of choice for solving the Puzzle:")
        print("1. Heuristic function h1 (number of tiles that are not in the correct place)")
        print("2. Heuristic function h2 (number of tiles that are not in the correct row plus number of tiles that are not in the correct column)")
        heuristic_choice = input("Enter your choice (1-2): ")

        # Execute the selected algorithm
        if choice == "1":
            print(f"\nInitial configuration: {start_state}\nUsing Greedy-Best First Search with h{heuristic_choice} heuristic")
            start = time.time()
            path, actions, entered_frontier, expanded = puzzle.greedy_best_first_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
        elif choice == "2":
            print(f"\nInitial configuration: {start_state}\nUsing A* Search with h{heuristic_choice} heuristic")
            start = time.time()
            path, actions, entered_frontier, expanded = puzzle.a_star_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
        else:
            print("Invalid input. Please enter correct numbers for input choices.")
            continue

        # Display results and statistics
        display_result(path, actions, entered_frontier, expanded, False)
        print(f"Search time: {end - start} seconds")