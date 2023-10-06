import time
import sys
import resource

class Search:

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def depth_limited_search(self, problem, depth_limit):
        # Initialize the frontier with the initial state
        frontier = [Node(problem.initial_state)]
        result = None  # Initialize result to None
        nodes_expanded = 0  # Initialize the count of expanded nodes

        while frontier:
            node = frontier.pop()  # Get the last node from the frontier (LIFO queue)
            nodes_expanded += 1  # Increment the count of expanded nodes

            if problem.is_goal(node.state):
                return node, nodes_expanded  # If the goal state is reached, return the solution node and nodes expanded

            if node.depth < depth_limit:
                # If the current node's depth is within the limit, expand it
                for move, child_state in problem.expand(node.state):
                    if not node.has_state(child_state):
                        child_node = Node(child_state, parent=node, depth=node.depth + 1, move=move)
                        frontier.append(child_node)  # Add child nodes to the frontier for further exploration

        return None, nodes_expanded  # If no solution found within the depth limit, return None and nodes expanded

    def iterative_deepening_search(self, problem):
        # Perform Iterative Deepening Depth-First Search (IDDFS)
        for depth in range(sys.maxsize):  # Iterate through increasing depth limits
            result, nodes_expanded = self.depth_limited_search(problem, depth)
            if result is not None:
                return result, nodes_expanded  # If a solution is found, return it and nodes expanded


    def solve(self, input_str):
        initial_state = input_str.split(" ")  # Split the input string into a list of numbers
        problem = FifteenPuzzleProblem(initial_state)  # Create a problem instance with the initial state

        start_time = time.time()  # Record the start time
        result, nodes_expanded = self.iterative_deepening_search(problem)  # Perform IDDFS search
        end_time = time.time()  # Record the end time

        if result:
            path = result.path()
            moves = "".join(move for move, _ in path[1:])  # Concatenate the moves as a string
            print("Moves:", moves)
            print("Number of Nodes expanded:", nodes_expanded)
            print("Time Taken:", end_time - start_time, "seconds")
            max_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # Max memory usage in kilobytes
            print("Max Memory (Bytes):", max_memory * 1024)  # Convert to bytes
            return moves  # Return the moves as a string
        else:
            print("No solution found.")
            return ""

class Node:
    def __init__(self, state, parent=None, depth=0, move=None):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.move = move

    def path(self):
        # Trace back the path from the current node to the root
        path_back = []
        node = self
        while node:
            path_back.append((node.move, node.state))
            node = node.parent
        return path_back[::-1]  # Reverse the path to get the correct order

    def has_state(self, other_state):
        if self.parent is None:
            return False
        if self.state == other_state:
            return True
        return self.parent.has_state(other_state)

class FifteenPuzzleProblem:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def is_goal(self, state):
        return state == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def expand(self, state):
        empty_index = state.index('0')
        moves = []

        if empty_index % 4 > 0:
            # Generate a new state by moving the empty tile to the left
            left_state = state[:]
            left_state[empty_index], left_state[empty_index - 1] = left_state[empty_index - 1], left_state[empty_index]
            moves.append(('L', left_state))

        if empty_index % 4 < 3:
            # Generate a new state by moving the empty tile to the right
            right_state = state[:]
            right_state[empty_index], right_state[empty_index + 1] = right_state[empty_index + 1], right_state[empty_index]
            moves.append(('R', right_state))

        if empty_index >= 4:
            # Generate a new state by moving the empty tile up
            up_state = state[:]
            up_state[empty_index], up_state[empty_index - 4] = up_state[empty_index - 4], up_state[empty_index]
            moves.append(('U', up_state))

        if empty_index < 12:
            # Generate a new state by moving the empty tile down
            down_state = state[:]
            down_state[empty_index], down_state[empty_index + 4] = down_state[empty_index + 4], down_state[empty_index]
            moves.append(('D', down_state))

        return moves

if __name__ == '__main__':
    agent = Search()
    input_str = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    agent.solve(input_str)
