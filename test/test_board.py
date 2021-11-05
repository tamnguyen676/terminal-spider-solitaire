import unittest
from src.board import *


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        board = Board()

        self.assertEquals(len(board.deck), 0)
        self.assertEquals(len(board.completed), 8)

        self.assertEquals(len(board.columns), 10)
        for i, column in enumerate(board.columns):
            if 1 <= i <= 4:
                self.assertEquals(len(column), 6)
            else:
                self.assertEquals(len(column), 5)

            for j, card in enumerate(column):
                if j != len(column) - 1:
                    self.assertFalse(card.revealed)
                else:
                    self.assertTrue(card.revealed)

        self.assertEquals(len(board.stock), 5)
        for i, stock in enumerate(board.stock):
            self.assertEquals(len(stock), 10)
            for j, card in enumerate(stock):
                self.assertFalse(card.revealed)
