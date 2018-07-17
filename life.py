'''
Conway's Game of Life

Excerpt from https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life:
Rules

    The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells,
    each of which is in one of two possible states, alive or dead, (or populated and unpopulated, respectively).
    Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically,
    or diagonally adjacent. At each step in time, the following transitions occur:

        Any live cell with fewer than two live neighbors dies, as if by under population.
        Any live cell with two or three live neighbors lives on to the next generation.
        Any live cell with more than three live neighbors dies, as if by overpopulation.
        Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

    The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules
    simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which
    this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules
    continue to be applied repeatedly to create further generations.
'''

# TODO: implement mouse clicks to stop/start/step evolution

from grid import Grid
from tkinter import Tk, Canvas, mainloop
import _thread
import random

class Life:
    def __init__(self, rows, cols):
        self.__grid = Grid(rows, cols)
        # window size
        self.x = 1024 # 640
        self.y = 768 # 480
        self.rows = rows
        self.cols = cols
        self.y_scale = self.y / rows
        self.x_scale = self.x / cols
        self.old_x = None
        self.old_y = None
        # corners of  the mandelbrot plan to display
        self.xa = -2.0
        self.xb = 1.0
        self.ya = -1.27
        self.yb = 1.27

        self.lock = _thread.allocate_lock()

        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.x, height=self.y, bg="#000000")
        self.canvas.pack()

    def create_test_scenario(self):
        seed_data = (
            (1, 1), (2, 2), (2, 3), (3, 1), (3, 2),
            (18, 14), (18, 15), (19, 14), (19, 15),
            (11, 14), (11, 15), (12, 14), (12, 15),
            # from https://stackoverflow.com/questions/9598552/a-suitable-game-of-life-seed-for-testing
            (52, 51), (53, 51), (55, 51), (56, 51),
            (53, 52), (55, 52),
            (53, 53), (55, 53),
            (52, 54), (53, 54), (55, 54), (56, 54),
            (51, 53), (52, 51), (52, 53), (53, 52), (53, 53)
        )

        # random grid
        seed_data = []
        for row in range(self.rows//3, self.rows//3*2):
            for col in range(self.cols//3, self.cols//3*2):
                if random.randint(0, 5) > 2:
                    seed_data.append((row, col))
        for cell in seed_data:
            self.__grid.set_alive(cell)

    def draw_cell(self, row, col):
        top_left_x = col * self.x_scale
        top_left_y = row * self.y_scale
        bottom_right_x = top_left_x + self.x_scale - 1
        bottom_right_y = top_left_y + self.y_scale - 1
        points = [top_left_x, top_left_y, bottom_right_x, top_left_y, bottom_right_x, bottom_right_y, top_left_x, bottom_right_y, top_left_x, top_left_y]
        self.canvas.create_polygon(points, fill='gray')

    def draw_empty(self, row, col):
        top_left_x = col * self.x_scale
        top_left_y = row * self.y_scale
        bottom_right_x = top_left_x + self.x_scale - 1
        bottom_right_y = top_left_y + self.y_scale - 1
        points = [top_left_x, top_left_y, bottom_right_x, top_left_y, bottom_right_x, bottom_right_y, top_left_x, bottom_right_y, top_left_x, top_left_y]
        self.canvas.create_polygon(points, fill='black')

    def draw_grid(self):
        self.canvas.delete('all')
        live_cells = self.__grid.get_live_cells()
        for cell in live_cells:
            self.draw_cell(cell[0], cell[1])

    def animate(self):
        self.__grid.tick()
        self.draw_grid()
        self.window.update()
        self.window.after(0, self.animate)

    def play(self):
        self.create_test_scenario()
        self.draw_grid()
        self.window.after_idle(self.animate)
        self.window.mainloop()


if __name__ == '__main__':
    scale = 5
    Life(768//scale, 1024//scale).play()