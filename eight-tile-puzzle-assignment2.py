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
            return self.copy_and_swap(state, x, y, x-1, y), "Up"
        return None, None

    def move_down(self, state):
        # Moves the blank tile down if possible.
        # Checks that the blank tile is not on the bottom row (x < self.n - 1) before swapping.
        x, y = self.find_blank(state)
        if x < self.n - 1:
            return self.copy_and_swap(state, x, y, x+1, y), "Down"
        return None, None

    def move_left(self, state):
        # Moves the blank tile left if possible.
        # Checks that the blank tile is not in the leftmost column (y > 0) before swapping.
        x, y = self.find_blank(state)
        if y > 0:
            return self.copy_and_swap(state, x, y, x, y-1), "Left"
        return None, None

    def move_right(self, state):
        # Moves the blank tile right if possible.
        # Checks that the blank tile is not in the rightmost column (y < self.n - 1) before swapping.
        x, y = self.find_blank(state)
        if y < self.n - 1:
            return self.copy_and_swap(state, x, y, x, y+1), "Right"
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
        # Implements Greedy Best-First Search algorithm using a heap (priority queue).
        # Initializes the root node containing starting state, no parent, and no action
        root = {"state": start, "parent": None, "action": None}

        # Create an empty list to act as the frontier (priority queue)
        # The counter is used as a tie breaker for equal priorities so a dict is used not as a tie breaker 
        frontier = []
        counter = 0

        # Condition so the heuristic chosen during the input is called during the search
        if heuristic == "1":
            heapq.heappush(frontier,(self.calculate_h1(start,goal), counter, root))
        else:
            heapq.heappush(frontier,(self.calculate_h2(start,goal), counter, root))
        
        # Initializes a set to keep track of explored states so they can be stored in a set
        explored = set([self.to_tuple(start)])
        #nodes_generated and nodes_expanded initialized to keep track of number of nodes expanded and generated
        nodes_generated = 1
        nodes_expanded = 0

        # Searches until frontier is empty or goal is found
        while frontier: 
            #takes Node with lost heuristic first (GFS condition) from the frontier
            _,_,node = heapq.heappop(frontier)
            nodes_expanded += 1
            state = node["state"]

            # Checks to see if current state is the goal state
            # if goal state, construct path and actions and return solution
            if state == goal:
                path, actions = self.reconstruct(node)
                return path, actions, nodes_generated, nodes_expanded
            

            # Expands current state with all possible successor statees
            # If a sucessor state has not been explored than compute its priority and store in the frontier
            for successor, action in self.expand_node(state):
                key = self.to_tuple(successor)
                if key not in explored:
                    # Marks state as explored to add revisiting it during the same search
                    explored.add(key) 
                    counter += 1
                    # Builds the new node with a link back to the parent and action for reconstructing solution
                    new_node = {"state": successor, "parent": node, "action": action}
                    # Calls the heuristic user chose to compute prioirity for newly expanded state
                    if heuristic == "1":
                        priority = self.calculate_h1(successor, goal)
                    else:
                        priority = self.calculate_h2(successor, goal)
                    # pushes new node to the frontier with priority, counter (to resolve tie breaks)
                    heapq.heappush(frontier, (priority, counter, new_node))
                    nodes_generated += 1

        # If frontier becomes empty without returning a solutoin, It returns none as no solution exists
        return None, None, nodes_generated, nodes_expanded




    def a_star_search(self, start, goal, heuristic):
        # Implements A* Search algorithm.
        root = {"state": start, "parent": None, "action": None}
        frontier = [root]               # Stack for DFS
        explored = set([self.to_tuple(start)])
        nodes_generated = 1
        nodes_expanded = 0

        while frontier:
            node = frontier.pop()      
            nodes_expanded += 1
            state = node["state"]

            # Check if the goal state is reached
            if state == goal:
                path, actions = self.reconstruct(node)
                return path, actions, nodes_generated, nodes_expanded

            # Reverse order to maintain consistent operator sequence
            for successor, action in reversed(self.expand_node(state)):
                key = self.to_tuple(successor)
                if key not in explored:
                    explored.add(key)
                    frontier.append({"state": successor, "parent": node, "action": action})
                    nodes_generated += 1

        return None, None, nodes_generated, nodes_expanded


def reshape(list_one, n):
    # Converts a 1D list into a 2D list.
    # Creates an empty board list to store rows.
    # For each row (from 0 to n-1), slice n values from the flat list in order.
    # Returns a 2D list representing the tile puzzle.
    board = []
    index = 0
    for _ in range(n):
        board.append(list_one[index:index+n])
        index += n
    return board

def display_result(path, actions, generated, expanded, print_steps = False):
    # Displays the solution path, actions, and search statistics.
    # Checks if a goal path exists. If it does not, it prints 'No solution found' and exits the function.
    # If a goal path exists, iterates over each state, printing the step number and board.
    # Uses len(actions)(sum of actions) as the path cost as each move has uniform cost of 1.
    # Finally prints nodes generated and expanded so algorithms can be compared by performance metrics.
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
    print("Nodes Generated:", generated)
    print("Nodes Expanded:", expanded)

if __name__ == "__main__":
    matrix_size = 3

    # The start_state is read from "input.txt" in the same folder as the code.
    # Program written and tested on macOS (reading input files on other OS may or may not work).
    with open('input.txt', 'r') as file:
        start_state = [int(number) for line in file for number in line.split()]

    # Manual entry for start state.
    # start_state = [8, 7, 6, 0, 4, 1, 2, 5, 3]
    goal_state  = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print(start_state)

    start_state_2d_form = reshape(start_state, matrix_size)
    goal_state_2d_form = reshape(goal_state, matrix_size)

    puzzle = TilePuzzle(start_state_2d_form)

    while True:
        print("\nSelect the algorithm to solve the Puzzle:")
        print("1. Greedy-Best First Search")
        print("2. A* Search")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        
        print("\nSelect the heuristic of choice for solving the Puzzle:")
        print("1. Heuristic function h1 (number of tiles that are not in the correct place)")
        print("2. Heuristic function h2 (number of tiles that are not in the correct row plus number of tiles that are not in the correct column)")

        heuristic_choice = input("Enter your choice (1-2): ")

        if choice == "1" and heuristic_choice == "1":
            print(f"\nInitial configuration: {start_state}\nUsing Greedy-Best First Search with h1")
            start = time.time()
            path, actions, generated, expanded = puzzle.greedy_best_first_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")
        
        elif choice == "1" and heuristic_choice == "2":
            print(f"\nInitial configuration: {start_state}\nUsing Greedy-Best First Search with h2")
            start = time.time()
            path, actions, generated, expanded = puzzle.greedy_best_first_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")

        elif choice == "2" and heuristic_choice == "1":
            print(f"\nInitial configuration: {start_state}\nUsing A* Search with h1")
            start = time.time()
            path, actions, generated, expanded = puzzle.a_star_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")
        
        elif choice == "2" and heuristic_choice == "2":
            print(f"\nInitial configuration: {start_state}\nUsing A* Search with h2")
            start = time.time()
            path, actions, generated, expanded = puzzle.a_star_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")

        elif choice == "3":
            break

        else:
            print("Invalid input. Please enter correct numbers for input choices")