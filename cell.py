'''
Call - single cell in Conway's Game of Life
'''

class Cell():
    Alive = 1
    Void = 0
    #status = Void

    def __init__(self, state):
        self.status = state
        self.age = 0

    def __repr__(self):
        if self.status == self.Alive:
            return "<Cell(Alive, age %d)>" % self.age
        else:
            return "<Cell(Void)>"

    def is_alive(self):
        return self.status == self.Alive

    def is_void(self):
        return self.status == self.Void

    def get_age(self):
        return self.age

    def add_age(self):
        if self.status == self.Alive: self.age += 1


## ####################################################################### ##
## UNIT TESTS

import unittest

class CellTests(unittest.TestCase):
    def test_create_live_cell(self):
        new_cell = Cell(Cell.Alive)
        self.assertEqual(new_cell.is_alive(), True)
        self.assertEqual(new_cell.is_void(), False)
        self.assertEqual(new_cell.get_age(), 0)
    def test_create_void_cell(self):
        new_cell = Cell(Cell.Void)
        self.assertEqual(new_cell.is_void(), True)
        self.assertEqual(new_cell.is_alive(), False)
    def test_age(self):
        new_cell = Cell(Cell.Alive)
        self.assertEqual(new_cell.get_age(), 0)
        new_cell.add_age()
        self.assertEqual(new_cell.get_age(), 1)

if __name__ == '__main__':
    unittest.main()