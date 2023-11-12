import threading
import tkinter as tk
from PIL import Image, ImageTk


class Board:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title("A Star")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.change_square_state)
        self.run_button = tk.Button(self.root, text="Run", command=self.run_star)
        self.run_button.pack(side="right")
        self.goal_button = tk.Button(self.root, text="Goal", command=self.set_goal)
        self.goal_button.pack(side="left")
        self.start_button = tk.Button(self.root, text="Start", command=self.set_start)
        self.start_button.pack(side="left")
        self.default_button = tk.Button(
            self.root, text="Wall", command=self.set_default
        )
        self.default_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        self.reset_button.pack(side="right")
        self.raw_mouse_image = Image.open("mouse.png")
        self.mouse_resize_image = self.raw_mouse_image.resize((30, 32))
        self.mouse_image = ImageTk.PhotoImage(self.mouse_resize_image)
        self.raw_cat_image = Image.open("cat.jpg")
        self.cat_resize_image = self.raw_cat_image.resize((39, 39))
        self.cat_image = ImageTk.PhotoImage(self.cat_resize_image)
        self.grid_size = 10
        self.selected_state = None
        self.start = None
        self.goal = None
        self.grid = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.player = "predator"
        self.update_grid()
        self.init_grid_from_board()

        self.predator_steps_entry = tk.Entry(self.root, width=5)
        self.predator_steps_entry.pack(side="right")
        self.predator_steps_label = tk.Label(self.root, text="Predator:")
        self.predator_steps_label.pack(side="right")
        self.predator_steps_entry.insert(0, "2")

        self.prey_steps_label = tk.Label(self.root, text="Prey:")
        self.prey_steps_label.pack(side="left")
        self.prey_steps_entry = tk.Entry(self.root, width=5)
        self.prey_steps_entry.pack(side="left")
        self.prey_steps_entry.insert(0, "1")

    def set_goal(self):
        self.selected_state = "goal"

    def set_start(self):
        self.selected_state = "start"

    def set_default(self):
        self.selected_state = None

    def update_grid(self):
        # self.canvas.delete("grid")
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square = self.board.get_square((x, y))
                if self.grid[x][y] != square.state:
                    if square.state == "wall":
                        color = "black"
                        self.canvas.create_rectangle(
                            x * 40,
                            y * 40,
                            (x + 1) * 40,
                            (y + 1) * 40,
                            fill=color,
                            outline="black",
                            tags="grid",
                        )
                    elif square.state == "path":
                        color = "blue"
                        self.canvas.create_rectangle(
                            x * 40,
                            y * 40,
                            (x + 1) * 40,
                            (y + 1) * 40,
                            fill=color,
                            outline="black",
                            tags="grid",
                        )
                    else:
                        color = "white"
                        self.canvas.create_rectangle(
                            x * 40,
                            y * 40,
                            (x + 1) * 40,
                            (y + 1) * 40,
                            fill=color,
                            outline="black",
                            tags="grid",
                        )
                self.grid[x][y] = square.state
        self.canvas.delete("mouse")
        if self.goal:
            self.canvas.create_image(
                self.goal[0] * 40 + 20,
                self.goal[1] * 40 + 20,
                image=self.mouse_image,
                tags="mouse",
            )
        self.canvas.delete("cat")
        if self.start:
            self.canvas.create_image(
                self.start[0] * 40 + 20,
                self.start[1] * 40 + 20,
                image=self.cat_image,
                tags="cat",
            )

    def init_grid_from_board(self):
        self.grid = [[None] * self.grid_size for _ in range(self.grid_size)]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square = self.board.get_square((x, y))
                if square:
                    self.grid[x][y] = square.state

    def change_square_state(self, event):
        x, y = event.x // 40, event.y // 40
        square = self.board.get_square((x, y))
        if square:
            if self.selected_state == "goal":
                if self.goal:
                    old_square = self.board.get_square(self.goal)
                    old_square.state = "empty"
                    old_square.f = 0
                    old_square.g = 0
                    old_square.h = 0
                    old_square.parent = None
                self.goal = (x, y)
                square.state = "goal"
                if square.f > 0:
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
            elif self.selected_state == "start":
                if self.start:
                    old_square = self.board.get_square(self.start)
                    old_square.state = "empty"
                    old_square.f = 0
                    old_square.g = 0
                    old_square.h = 0
                    old_square.parent = None
                self.start = (x, y)
                square.state = "start"
                if square.f > 0:
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
            else:
                if square.state == "wall":
                    square.state = "empty"
                elif square.state == "empty":
                    square.state = "wall"
                elif square.state == "path":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                elif square.state == "goal":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                    self.goal = None
                elif square.state == "start":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                    self.start = None
            self.update_grid()

    def run_star(self):
        predator_steps = int(self.predator_steps_entry.get()) + 1
        prey_steps = int(self.prey_steps_entry.get()) + 1

        self.clear_grid_except_start_goal()
        self.update_grid()

        def a_star_thread():
            path_found = self.board.execute_a_star(
                self.start, self.goal, self, predator_steps, prey_steps
            )
            if path_found:
                print("Predador encontrou a presa")
            else:
                self.update_grid()
                print("Predador não encontrou a presa")

        thread = threading.Thread(target=a_star_thread)
        thread.start()
        self.player = "predator"

    def clear_grid_except_start_goal(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square = self.board.get_square((x, y))
                if (
                    square
                    and square.state != "start"
                    and square.state != "goal"
                    and square.state != "wall"
                ):
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
        self.update_grid()

    def highlight_path_on_grid(self, path):
        for x, y in path:
            square = self.board.get_square((x, y))
            if square and square.state != "goal" and square.state != "start":
                square.state = "path"
        self.update_grid()

    def reset_board(self):
        self.board.reset_to_initial_state()
        self.goal = None
        self.start = None
        self.selected_state = None
        self.update_grid()

    def render(self):
        self.root.mainloop()
