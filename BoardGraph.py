import time
from Board import Board
from Square import Square


class BoardGraph:
    def __init__(self):
        self.graph = {}
        self.create_initial_board(10)

    def add_square(self, coordinates):
        if coordinates not in self.graph:
            new_square = Square(*coordinates)
            self.graph[coordinates] = new_square

    def get_square(self, coordinates):
        if coordinates in self.graph:
            return self.graph[coordinates]
        else:
            return None

    def add_neighbors(self, x, y):
        if (x, y) in self.graph:
            square = self.graph[(x, y)]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_x, new_y = x + dx, y + dy
                    if (new_x, new_y) in self.graph:
                        square.add_neighbor((new_x, new_y))

    def create_initial_board(self, size=10):
        for x in range(size):
            for y in range(size):
                self.add_square((x, y))
        for x in range(size):
            for y in range(size):
                self.add_neighbors(x, y)

    def build_path_from_goal(self, goal):
        path = []
        current = self.graph[goal]

        while current:
            path.append((current.x, current.y))
            current = current.parent

        return path[::-1]

    def execute_a_star(self, start, goal, board_i: Board, predator_steps, prey_steps):
        open_set = set()
        closed_set = set()
        start_square = self.graph[start]
        goal_square = self.graph[goal]

        start_square.g = 0
        start_square.h = self.calculate_h(start_square, goal_square)
        start_square.f = start_square.h + start_square.g

        open_set.add(start)
        count = 0
        while open_set:
            board_i.update_grid()
            time.sleep(1)

            if board_i.player == "predator":
                current = self.find_lowest_f(open_set)
                board_i.start = (current.x, current.y)
                count += 1
                if count == predator_steps:
                    break
            else:
                current = self.find_largest_f(open_set)
                board_i.goal = (current.x, current.y)
                count += 1
                if count == prey_steps:
                    break

            if current == goal:
                return True

            open_set.remove(current)
            closed_set.add(current)

            for neighbor_coordinates in self.graph[current].neighbors:
                neighbor = self.graph[neighbor_coordinates]

                if neighbor_coordinates in closed_set or neighbor.state == "wall":
                    continue

                tentative_g = self.calculate_g(current, neighbor)

                if neighbor_coordinates not in open_set:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = self.calculate_h(neighbor, goal_square)
                    neighbor.f = neighbor.g + neighbor.h

                    open_set.add(neighbor_coordinates)

                elif tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + neighbor.h

        board_i.player = "prey" if board_i.player == "predator" else "predator"
        for square in self.graph.values():
            square.f = 0
            square.g = 0
            square.h = 0
        if board_i.player == "predator":
            return self.execute_a_star(
                board_i.start, board_i.goal, board_i, predator_steps, prey_steps
            )
        else:
            return self.execute_a_star(
                board_i.goal, board_i.start, board_i, predator_steps, prey_steps
            )

    def calculate_g(self, current, neighbor, diagonal_cost=14, orthogonal_cost=10):
        dx = abs(current.x - neighbor.x)
        dy = abs(current.y - neighbor.y)

        if dx == 1 and dy == 1:
            return diagonal_cost + current.g
        else:
            return orthogonal_cost + current.g

    def calculate_h(self, neighbor, goal_square, D=10):
        dx = abs(neighbor.x - goal_square.x)
        dy = abs(neighbor.y - goal_square.y)
        return D * (dx + dy)

    def find_lowest_f(self, open_set):
        lowest_f_square = None
        lowest_f_value = float("inf")

        for square_coordinates in open_set:
            square = self.graph[square_coordinates]
            if square.f < lowest_f_value:
                lowest_f_square = square
                lowest_f_value = square.f

        return lowest_f_square

    def find_largest_f(self, open_set):
        largest_f_square = None
        largest_f_value = -1

        for square_coordinates in open_set:
            square = self.graph[square_coordinates]
            if square.f > largest_f_value:
                largest_f_square = square
                largest_f_value = square.f

        return largest_f_square

    def reset_to_initial_state(self):
        for square in self.graph.values():
            square.f = 0
            square.g = 0
            square.h = 0
            square.state = "empty"
            square.parent = None
