'''
Grid - grid array of Comway's Game of Life Cells
'''

# TODO: would a linked cell be quicker than discovery?

from cell import Cell
import copy
import random

class Grid:
    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.__grid = {}

    def __repr__(self):
        return "<Grid(%dx%d, %d cells)>" % (self.__rows, self.__cols, self.num_cells())

    def num_cells(self):
        return len(self.__grid)

    def set_alive(self, coords):
        self.__grid[coords] = Cell(Cell.Alive)

    def set_void(self, coords):
        if coords in self.__grid: del self.__grid[coords]

    def is_alive(self, coords):
        return coords in self.__grid and self.__grid[coords].is_alive()

    def is_void(self, coords):
        return not coords in self.__grid or self.__grid[coords].is_void()

    def get_neighbours(self, coords):
        row = coords[0]
        col = coords[1]
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

    def count_live_neighbours(self, coords):
        num_neighbours = 0
        neighbours = self.get_neighbours(coords)
        for neighbour in neighbours.keys():
            if self.is_alive(neighbour):
                num_neighbours += 1
        return num_neighbours

    def get_live_cells(self):
        live_cells = []
        for cell in self.__grid.keys():
            live_cells.append(cell)
        return live_cells

    def tick(self):
        # Compute next generation of cells
        # 1. go through each live cell
        # 1.1 apply rules 1 and 3 to see if it dies
        # 1.2 check neighbouring cells ... should they spawn?
        checked_cells = copy.deepcopy(self.__grid)
        new_grid = copy.deepcopy(self.__grid)
        for coords in self.__grid.keys():
            live_neighbours = self.count_live_neighbours(coords)
            if live_neighbours < 2:   # rule 1: <2 ... cell dies
                del new_grid[coords]
            #elif live_neighbours == 4:  # MADEUP rule ... random!
            #    if random.randint(0, 2): del new_grid[coords]
            elif live_neighbours > 3:   # rule 3: >3 ... cell dies
                del new_grid[coords]
            checked_cells[coords] = 1

            neighbours = self.get_neighbours(coords)
            for coords in neighbours.keys():
                if coords in checked_cells: continue  # already checked
                live_neighbours = self.count_live_neighbours(coords)
                if live_neighbours == 3:  # rule 4: ==3 ... cell born
                    new_grid[coords] = Cell(Cell.Alive)
                checked_cells[coords] = 1

        self.__grid = new_grid

    def as_grid_string(self):
        return '\n'.join([''.join(['#' if self.is_alive((row, col)) else ' ' for row in range(self.__rows)]) for col in range(self.__cols)])

## ####################################################################### ##

import unittest

class CellTests(unittest.TestCase):
    def create_test_scenario(self):
        grid = Grid(10,10)
        grid.set_alive((1, 1))
        grid.set_alive((2, 2))
        grid.set_alive((2, 3))
        grid.set_alive((3, 1))
        grid.set_alive((3, 2))
        return grid

    def test_create_grid(self):
        grid = self.create_test_scenario()
        self.assertTrue(grid)
        self.assertEqual(grid.count_live_neighbours((0, 0)), 1)
        self.assertEqual(grid.count_live_neighbours((0, 0)), 1)
        self.assertEqual(grid.count_live_neighbours((0, 1)), 1)
        self.assertEqual(grid.count_live_neighbours((0, 2)), 1)
        self.assertEqual(grid.count_live_neighbours((0, 3)), 0)
        self.assertEqual(grid.count_live_neighbours((0, 4)), 0)
        self.assertEqual(grid.count_live_neighbours((1, 0)), 1)
        self.assertEqual(grid.count_live_neighbours((1, 2)), 3)
        self.assertEqual(grid.count_live_neighbours((1, 3)), 2)
        self.assertEqual(grid.count_live_neighbours((1, 4)), 1)
        self.assertEqual(grid.count_live_neighbours((2, 0)), 2)
        self.assertEqual(grid.count_live_neighbours((2, 1)), 4)
        self.assertEqual(grid.count_live_neighbours((2, 4)), 1)
        self.assertEqual(grid.count_live_neighbours((3, 0)), 1)
        self.assertEqual(grid.count_live_neighbours((3, 3)), 3)
        self.assertEqual(grid.count_live_neighbours((3, 4)), 1)
        self.assertEqual(grid.count_live_neighbours((4, 0)), 1)
        self.assertEqual(grid.count_live_neighbours((4, 1)), 2)
        self.assertEqual(grid.count_live_neighbours((4, 2)), 2)
        self.assertEqual(grid.count_live_neighbours((4, 3)), 1)
        self.assertEqual(grid.count_live_neighbours((4, 4)), 0)
        print(grid.as_grid_string())
        grid.tick()
        print(grid.as_grid_string())
        self.assertTrue(grid.is_void((1, 1)))
        self.assertTrue(grid.is_alive((1, 2)))
        self.assertTrue(grid.is_void((2, 2)))
        self.assertTrue(grid.is_alive((2, 3)))
        self.assertTrue(grid.is_alive((3, 1)))
        self.assertTrue(grid.is_alive((3, 2)))
        self.assertTrue(grid.is_alive((3, 3)))

if __name__ == '__main__':
    unittest.main()