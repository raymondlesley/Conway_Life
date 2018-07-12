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

from grid import Grid
from tkinter import Tk, Canvas, mainloop

class Life:
    def __init__(self, rows, cols):
        self.__grid = Grid(rows, cols)
        # window size
        self.x = 640
        self.y = 480
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

        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.x, height=self.y, bg="#000000")
        self.canvas.pack()

    def create_test_scenario(self):
        self.__grid.set_alive(1, 1)
        self.__grid.set_alive(2, 2)
        self.__grid.set_alive(2, 3)
        self.__grid.set_alive(3, 1)
        self.__grid.set_alive(3, 2)

        self.__grid.set_alive(18, 14)
        self.__grid.set_alive(18, 15)
        self.__grid.set_alive(19, 14)
        self.__grid.set_alive(19, 15)

        self.__grid.set_alive(11, 14)
        self.__grid.set_alive(11, 15)
        self.__grid.set_alive(12, 14)
        self.__grid.set_alive(12, 15)

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
        #self.__grid.tick()


if __name__ == '__main__':
    Life(80, 100).play()