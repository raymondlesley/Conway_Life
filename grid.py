'''
Grid - grid array of Comway's Game of Life Cells
'''

# TODO: refactor calls to accept coords tuples instead of row, col
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

    def get_neighbours(self, row, col):
        neighbours = {}
        if row > 0:
            neighbours[(row - 1, col)] = 1
            if col > 0:
                neighbours[(row - 1, col - 1)] = 1
            if col < (self.__cols - 1):
                neighbours[(row - 1, col + 1)] = 1
        if row < (self.__rows - 1):
            neighbours[(row + 1, col)] = 1
            if col > 0:
                neighbours[(row + 1, col - 1)] = 1
            if col < (self.__cols - 1):
                neighbours[(row + 1, col + 1)] = 1
        if col > 0:
            neighbours[(row, col - 1)] = 1
        if col < (self.__cols - 1):
            neighbours[(row, col + 1)] = 1
        return neighbours

    def count_live_neighbours(self, row, col):
        num_neighbours = 0
        neighbours = self.get_neighbours(row, col)
        for neighbour, dummy in neighbours.items():  # TODO: can you just get keys?
            if self.is_alive(neighbour[0], neighbour[1]):
                num_neighbours += 1
        return num_neighbours

    def tick(self):
        # Compute next generation of cells
        # 1. go through each live cell
        # 1.1 apply rules 1 and 3 to see if it dies
        # 1.2 check neighbouring cells ... should they spawn?
        checked_cells = copy.deepcopy(self.__grid)
        new_grid = copy.deepcopy(self.__grid)
        for coords, cell in self.__grid.items():  # TODO: can you just get keys?
            live_neighbours = self.count_live_neighbours(coords[0], coords[1])
            if live_neighbours < 2:   # rule 1: <2 ... cell dies
                del new_grid[coords]
            elif live_neighbours > 3:   # rule 3: >3 ... cell dies
                del new_grid[coords]
            checked_cells[coords] = 1

            neighbours = self.get_neighbours(coords[0], coords[1])
            for coords, neighbour in neighbours.items():  # TODO: can you just get keys?
                if coords in checked_cells: continue  # already checked
                live_neighbours = self.count_live_neighbours(coords[0], coords[1])
                if live_neighbours == 3:  # rule 4: ==3 ... cell born
                    new_grid[coords] = Cell(Cell.Alive)
                checked_cells[coords] = 1

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
        self.assertEqual(grid.count_live_neighbours(0, 0), 1)
        self.assertEqual(grid.count_live_neighbours(0, 0), 1)
        self.assertEqual(grid.count_live_neighbours(0, 1), 1)
        self.assertEqual(grid.count_live_neighbours(0, 2), 1)
        self.assertEqual(grid.count_live_neighbours(0, 3), 0)
        self.assertEqual(grid.count_live_neighbours(0, 4), 0)
        self.assertEqual(grid.count_live_neighbours(1, 0), 1)
        self.assertEqual(grid.count_live_neighbours(1, 2), 3)
        self.assertEqual(grid.count_live_neighbours(1, 3), 2)
        self.assertEqual(grid.count_live_neighbours(1, 4), 1)
        self.assertEqual(grid.count_live_neighbours(2, 0), 2)
        self.assertEqual(grid.count_live_neighbours(2, 1), 4)
        self.assertEqual(grid.count_live_neighbours(2, 4), 1)
        self.assertEqual(grid.count_live_neighbours(3, 0), 1)
        self.assertEqual(grid.count_live_neighbours(3, 3), 3)
        self.assertEqual(grid.count_live_neighbours(3, 4), 1)
        self.assertEqual(grid.count_live_neighbours(4, 0), 1)
        self.assertEqual(grid.count_live_neighbours(4, 1), 2)
        self.assertEqual(grid.count_live_neighbours(4, 2), 2)
        self.assertEqual(grid.count_live_neighbours(4, 3), 1)
        self.assertEqual(grid.count_live_neighbours(4, 4), 0)
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