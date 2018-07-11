'''
Call - single cell in Conway's Game of Life
'''

class Cell():
    Alive = 1
    Void = 0
    #status = Void

    def __init__(self, state):
        self.status = state

    def __repr__(self):
        if self.status == self.Alive:
            return "<Cell(Alive)>"
        else:
            return "<Cell(Void)>"

    def is_alive(self):
        return self.status == self.Alive

    def is_void(self):
        return self.status == self.Void

## ####################################################################### ##
## UNIT TESTS

import unittest

class CellTests(unittest.TestCase):
    def test_create_live_cell(self):
        new_cell = Cell(Cell.Alive)
        self.assertEqual(new_cell.is_alive(), True)
        self.assertEqual(new_cell.is_void(), False)
    def test_create_void_cell(self):
        new_cell = Cell(Cell.Void)
        self.assertEqual(new_cell.is_void(), True)
        self.assertEqual(new_cell.is_alive(), False)

if __name__ == '__main__':
    unittest.main()