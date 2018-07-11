'''
Grid - grid array of Comway's Game of Life Cells
'''

# TODO: this is in effcient, as most cells are empty - but need to be processed
# TODO: use a sparse data set (dict?)
# TODO: simple d[(x,y)] = 1 and (x.y) in d (no need for boundary checks!)
# TODO: how to test empty cells?
# TODO: suggestion: walk around live cells; keep a record of which checked...
# TODO: would a linked cell be quicker than discovery?

from cell import Cell
import copy

class Grid:
    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.__grid = [[Cell(Cell.Void) for col in range(cols)] for row in range(rows)]

    def __repr__(self):
        return "<Grid(%dx%d)>" % (self.__rows, self.__cols)

    def set_alive(self, row, col):
        self.__grid[row][col] = Cell(Cell.Alive)

    def set_void(self, row, col):
        self.__grid[row][col] = Cell(Cell.Void)

    def is_alive(self, row, col):
        return self.__grid[row][col].is_alive()

    def is_void(self, row, col):
        return self.__grid[row][col].is_void()

    def adjacent_live_cells(self, row, col):
        num_live_cells = 0
        if row > 0:
            if self.__grid[row - 1][col].is_alive(): num_live_cells += 1            # N
            if col > 0:
                if self.__grid[row - 1][col - 1].is_alive(): num_live_cells += 1    # NW
            if col < (self.__cols - 1):
                if self.__grid[row - 1][col + 1].is_alive(): num_live_cells += 1    # NE
        if row < (self.__rows - 1):
            if self.__grid[row + 1][col].is_alive(): num_live_cells += 1            # S
            if col > 0:
                if self.__grid[row + 1][col - 1].is_alive(): num_live_cells += 1    # SW
            if col < (self.__cols - 1):
                if self.__grid[row + 1][col + 1].is_alive(): num_live_cells += 1    # SE
        if col > 0:
            if self.__grid[row][col - 1].is_alive(): num_live_cells += 1            # W
        if col < (self.__cols - 1):
            if self.__grid[row][col + 1].is_alive(): num_live_cells += 1            # E
        return num_live_cells

    def tick(self):
        """Compute next generation of cells"""
        new_grid = copy.deepcopy(self.__grid)
        for row in range(self.__rows):
            for col in range(self.__cols):
                cell = self.__grid[row][col]
                num_adjent_live_cells = self.adjacent_live_cells(row, col)
                if cell.is_alive():
                    if num_adjent_live_cells < 2:   # rule 1: <2 ... cell dies
                        new_grid[row][col] = Cell(Cell.Void)
                    elif num_adjent_live_cells > 3:   # rule 3: >3 ... cell dies
                        new_grid[row][col] = Cell(Cell.Void)
                elif num_adjent_live_cells == 3:   # rule 4: ==3 ... cell born
                    new_grid[row][col] = Cell(Cell.Alive)
        self.__grid = new_grid


    def as_grid_string(self):
        return '\n'.join([''.join(['#' if self.__grid[row][col].is_alive() else ' ' for row in range(self.__rows)]) for col in range(self.__cols)])

## ####################################################################### ##

import unittest

class CellTests(unittest.TestCase):
    def create_test_scenario(self):
        grid = Grid(10,10)
        grid.set_alive(1, 1)
        grid.set_alive(2, 2)
        grid.set_alive(2, 3)
        grid.set_alive(3, 1)
        grid.set_alive(3, 2)
        return grid

    def test_create_grid(self):
        grid = self.create_test_scenario()
        self.assertTrue(grid)
        self.assertTrue(grid.adjacent_live_cells(0, 0) == 1)
        self.assertTrue(grid.adjacent_live_cells(0, 1) == 1)
        self.assertTrue(grid.adjacent_live_cells(0, 2) == 1)
        self.assertTrue(grid.adjacent_live_cells(0, 3) == 0)
        self.assertTrue(grid.adjacent_live_cells(0, 4) == 0)
        self.assertTrue(grid.adjacent_live_cells(1, 0) == 1)
        self.assertTrue(grid.adjacent_live_cells(1, 2) == 3)
        self.assertTrue(grid.adjacent_live_cells(1, 3) == 2)
        self.assertTrue(grid.adjacent_live_cells(1, 4) == 1)
        self.assertTrue(grid.adjacent_live_cells(2, 0) == 2)
        self.assertTrue(grid.adjacent_live_cells(2, 1) == 4)
        self.assertTrue(grid.adjacent_live_cells(2, 4) == 1)
        self.assertTrue(grid.adjacent_live_cells(3, 0) == 1)
        self.assertTrue(grid.adjacent_live_cells(3, 3) == 3)
        self.assertTrue(grid.adjacent_live_cells(3, 4) == 1)
        self.assertTrue(grid.adjacent_live_cells(4, 0) == 1)
        self.assertTrue(grid.adjacent_live_cells(4, 1) == 2)
        self.assertTrue(grid.adjacent_live_cells(4, 2) == 2)
        self.assertTrue(grid.adjacent_live_cells(4, 3) == 1)
        self.assertTrue(grid.adjacent_live_cells(4, 4) == 0)
        print(grid.as_grid_string())
        grid.tick()
        print(grid.as_grid_string())
        self.assertTrue(grid.is_void(1, 1))
        self.assertTrue(grid.is_alive(1, 2))
        self.assertTrue(grid.is_void(2, 2))
        self.assertTrue(grid.is_alive(2, 3))
        self.assertTrue(grid.is_alive(3, 1))
        self.assertTrue(grid.is_alive(3, 2))
        self.assertTrue(grid.is_alive(3, 3))

if __name__ == '__main__':
    unittest.main()