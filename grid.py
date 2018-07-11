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
        self.__grid = {}

    def __repr__(self):
        return "<Grid(%dx%d)>" % (self.__rows, self.__cols)

    def set_alive(self, row, col):
        self.__grid[(row, col)] = Cell(Cell.Alive)

    def set_void(self, row, col):
        key = (row, col)
        if key in self.__grid: del self.__grid[key]

    def is_alive(self, row, col):
        key = (row, col)
        return key in self.__grid and self.__grid[key].is_alive()

    def is_void(self, row, col):
        key = (row, col)
        return not key in self.__grid or self.__grid[key].is_void()

    def count_neighbours(self, row, col):
        num_live_cells = 0
        if row > 0:
            if self.is_alive(row - 1, col): num_live_cells += 1            # N
            if col > 0:
                if self.is_alive(row - 1, col - 1): num_live_cells += 1    # NW
            if col < (self.__cols - 1):
                if self.is_alive(row - 1, col + 1): num_live_cells += 1    # NE
        if row < (self.__rows - 1):
            if self.is_alive(row + 1, col): num_live_cells += 1            # S
            if col > 0:
                if self.is_alive(row + 1, col - 1): num_live_cells += 1    # SW
            if col < (self.__cols - 1):
                if self.is_alive(row + 1, col + 1): num_live_cells += 1    # SE
        if col > 0:
            if self.is_alive(row, col - 1): num_live_cells += 1            # W
        if col < (self.__cols - 1):
            if self.is_alive(row, col + 1): num_live_cells += 1            # E
        return num_live_cells

    def tick(self):
        """Compute next generation of cells"""
        new_grid = copy.deepcopy(self.__grid)
        for row in range(self.__rows):
            for col in range(self.__cols):
                cell = self.__grid.get((row, col))
                num_adjent_live_cells = self.count_neighbours(row, col)
                if cell and cell.is_alive():
                    if num_adjent_live_cells < 2:   # rule 1: <2 ... cell dies
                        del new_grid[(row, col)]
                    elif num_adjent_live_cells > 3:   # rule 3: >3 ... cell dies
                        del new_grid[(row, col)]
                elif num_adjent_live_cells == 3:   # rule 4: ==3 ... cell born
                    new_grid[(row, col)] = Cell(Cell.Alive)
        self.__grid = new_grid


    def as_grid_string(self):
        return '\n'.join([''.join(['#' if self.is_alive(row, col) else ' ' for row in range(self.__rows)]) for col in range(self.__cols)])

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
        self.assertTrue(grid.count_neighbours(0, 0) == 1)
        self.assertTrue(grid.count_neighbours(0, 1) == 1)
        self.assertTrue(grid.count_neighbours(0, 2) == 1)
        self.assertTrue(grid.count_neighbours(0, 3) == 0)
        self.assertTrue(grid.count_neighbours(0, 4) == 0)
        self.assertTrue(grid.count_neighbours(1, 0) == 1)
        self.assertTrue(grid.count_neighbours(1, 2) == 3)
        self.assertTrue(grid.count_neighbours(1, 3) == 2)
        self.assertTrue(grid.count_neighbours(1, 4) == 1)
        self.assertTrue(grid.count_neighbours(2, 0) == 2)
        self.assertTrue(grid.count_neighbours(2, 1) == 4)
        self.assertTrue(grid.count_neighbours(2, 4) == 1)
        self.assertTrue(grid.count_neighbours(3, 0) == 1)
        self.assertTrue(grid.count_neighbours(3, 3) == 3)
        self.assertTrue(grid.count_neighbours(3, 4) == 1)
        self.assertTrue(grid.count_neighbours(4, 0) == 1)
        self.assertTrue(grid.count_neighbours(4, 1) == 2)
        self.assertTrue(grid.count_neighbours(4, 2) == 2)
        self.assertTrue(grid.count_neighbours(4, 3) == 1)
        self.assertTrue(grid.count_neighbours(4, 4) == 0)
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