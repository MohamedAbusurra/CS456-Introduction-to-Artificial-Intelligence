import time
import heapq

class TilePuzzle:
    def __init__(self, tile_board):
        # Initializes the puzzle board and stores its size
        self.board = [row[:] for row in tile_board]
        self.n = len(tile_board)

    def find_blank(self, state):
        # Locates the position of the blank (0) in the puzzle
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:
                    return i, j
        return None  # Added for safety, There should always be exactly one blank

    def copy_and_swap(self, state, x1, y1, x2, y2):
        # Creates a copy of the board and swaps the two given positions
        successor = [row[:] for row in state]
        successor[x1][y1], successor[x2][y2] = successor[x2][y2], successor[x1][y1]
        return successor
    
    def calculate_h1(self, successor, goal_state):

        heuristic_one = 0 
        # Traverse the generated tile row by row 
        # Ignore zero which is the empty tile 
        # check the value of the generated state with the goal state at each position
        # If the values do not match the heuristic is incremented by one
        for i in range(len(successor)):
            for j in range(len(successor[i])):
                if successor[i][j] != goal_state[i][j] and successor[i][j] != 0:
                   heuristic_one += 1
        print(heuristic_one)

        return heuristic_one
    
    
    def calculate_h2(self, successor, goal_state):
        heuristic_two = 0

        # Traverse the generated tile row by row (row_major order)
        # Ignore zero which is the empty tile 
        # At each iteration a goal_row list is generated containing the values present in the goal_state at that row 
        # Each generated state row value is checked to see if it is contained in the goal_state row list
        # If it is not present the heuristic is incremented by one
        for i in range(len(successor)):
            goal_row = goal_state[i]
            for j in range(len(successor[i])):
                if successor[i][j] not in goal_row and successor[i][j] != 0:
                   heuristic_two += 1

        # Traverse the generated tile column by column (column-major order)
        # Ignore zero which is the empty tile 
        # At each iteration a col_row list is generated containing the values present in the goal_state at that col 
        # Each generated state col value is checked to see if it is contained in the goal_state col list
        # If it is not present the heuristic is incremented by one
        for j in range(len(successor[0])):
            goal_col = [row[j] for row in goal_state]
            for i in range(len(successor)):
                if successor[i][j] not in goal_col and successor[i][j] != 0:
                   heuristic_two += 1

        return heuristic_two
    

    def to_tuple(self, state):
        # Converts board to an immutable tuple form to allow for use in sets
        return tuple(tuple(row) for row in state)

    def move_up(self, state):
        # Moves the blank tile up if possible
        x, y = self.find_blank(state)
        if x > 0:
            return self.copy_and_swap(state, x, y, x-1, y), "Up"
        return None, None

    def move_down(self, state):
        # Moves the blank tile down if possible
        x, y = self.find_blank(state)
        if x < self.n - 1:
            return self.copy_and_swap(state, x, y, x+1, y), "Down"
        return None, None

    def move_left(self, state):
        # Moves the blank tile left if possible
        x, y = self.find_blank(state)
        if y > 0:
            return self.copy_and_swap(state, x, y, x, y-1), "Left"
        return None, None

    def move_right(self, state):
        # Moves the blank tile right if possible
        x, y = self.find_blank(state)
        if y < self.n - 1:
            return self.copy_and_swap(state, x, y, x, y+1), "Right"
        return None, None

    def expand_node(self, state):
        # Generates all possible successor states from the current state
        successors = []
        for operator in [self.move_up, self.move_down, self.move_left, self.move_right]:
            successor, action = operator(state)
            if successor is not None:
                successors.append((successor, action))
        return successors

    def reconstruct(self, node):
        # Reconstructs the path and actions from the goal back to the start
        states, actions = [], []
        current = node
        while current is not None:
            states.append(current["state"])
            actions.append(current["action"])
            current = current["parent"]
        states.reverse()
        actions.reverse()
        return states, actions[1:]  # Skip the initial None action from root

    def greedy_best_first_search(self, start, goal, heuristic):
        # Implements greedy best first Search algorithm
        root = {"state": start, "parent": None, "action": None}
        frontier = []
        heapq.heappush(frontier,root)
        explored = set([self.to_tuple(start)]) 
        nodes_generated = 1
        nodes_expanded = 0

        while frontier:
            _ , node = heapq.heappop(frontier)
            nodes_expanded += 1
            state = node["state"]

            # Check if the goal state is reached
            if state == goal:
                path, actions = self.reconstruct(node)
                return path, actions, nodes_generated, nodes_expanded

            # Expand the current node and add unseen states to frontier
            for successor, action in self.expand_node(state):
                key = self.to_tuple(successor)
                if key not in explored:
                    explored.add(key)
                    frontier.append(self.h1(successor, goal),{"state": successor, "parent": node, "action": action})
                    nodes_generated += 1

        return None, None, nodes_generated, nodes_expanded

    def a_star_search(self, start, goal, heuristic):
        # Implements A* Search algorithm
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


def reshape(flat_list, n):
    # Converts a 1D list into a 2D list
    board = []
    idx = 0
    for _ in range(n):
        board.append(flat_list[idx:idx+n])
        idx += n
    return board

def display_result(path, actions, generated, expanded):
    # Displays the solution path, actions, and search statistics
    if path is None:
        print("No solution found.\n")
        return
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
        print("1. Heuristic function h2 (number of tiles that are not in the correct row plus number of tiles that are not in the correct column)")

        heuristic_choice = input("Enter your choice (1-2): ")

        if choice == "1" and heuristic_choice == "1":
            print(f"\nInitial configuration: {start_state}\nUsing Greedy-Best First Search with h1:")
            start = time.time()
            path, actions, generated, expanded = puzzle.greedy_best_first_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")
        
        if choice == "1" and heuristic_choice == "2":
            print(f"\nInitial configuration: {start_state}\nUsing Greedy-Best First Search with h2:")
            start = time.time()
            path, actions, generated, expanded = puzzle.greedy_best_first_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")

        elif choice == "2" and heuristic_choice == "1":
            print(f"\nInitial configuration: {start_state}\nUsing A* Search with h1:")
            start = time.time()
            path, actions, generated, expanded = puzzle.a_star_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")
        
        elif choice == "2" and heuristic_choice == "2":
            print(f"\nInitial configuration: {start_state}\nUsing A* Search with h2:")
            start = time.time()
            path, actions, generated, expanded = puzzle.a_star_search(start_state_2d_form, goal_state_2d_form, heuristic_choice)
            end = time.time()
            display_result(path, actions, generated, expanded)
            print(f"Search time: {end - start} seconds")

        elif choice == "3":
            break

        else:
            print("Invalid input. Please enter correct numbers for input choices")