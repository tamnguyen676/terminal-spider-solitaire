import unittest
from src.board import Column
from src.game_engine import *
from src.deck import Card, Suit


class TestGameEngine(unittest.TestCase):
    game_engine = None

    @classmethod
    def setUpClass(cls):
        cls.game_engine = GameEngine(suits=1)

    def test_find_best_row_idx(self):
        cards = [Card(5, Suit.club, False), Card(4, Suit.club, True), Card(3, Suit.club, True), Card(2, Suit.club, True)]
        col = Column(cards)
        TestGameEngine.game_engine.board.columns[1] = col
        self.assertEquals(self.game_engine.find_best_row_idx(1), 1)

        cards = [Card(7, Suit.club, True), Card(6, Suit.club, True), Card(3, Suit.club, True), Card(2, Suit.club, True)]
        col = Column(cards)
        TestGameEngine.game_engine.board.columns[1] = col
        self.assertEquals(self.game_engine.find_best_row_idx(1), 2)

    def test_move_cards(self):
        board = Board()
        col1_cards = [Card(10, Suit.club, True), Card(8, Suit.club, True), Card(7, Suit.club, True),
                      Card(6, Suit.club, True)]
        col2_cards = [Card(9, Suit.club, True)]

        board.columns[1] = Column(col1_cards)
        board.columns[2] = Column(col2_cards)

        self.game_engine.board = board

        self.game_engine.move_cards(1, 1, 2)
        self.assertEqual(len(board.columns[1]), 1)
        self.assertEqual(len(board.columns[2]), 4)

    def test_hold_cards(self):
        board = Board()
        col1_cards = [Card(10, Suit.club, True), Card(8, Suit.club, True), Card(7, Suit.club, True),
                      Card(6, Suit.club, True)]
        column1 = Column(col1_cards)
        board.columns[1] = column1

        self.game_engine.board = board

        self.game_engine.hold_cards(1, 1)
        self.assertFalse(board.columns[1][0].holding)
        for i in range(1, len(col1_cards)):
            self.assertTrue(board.columns[1][i].holding)

    def test_find_best_col_to_place(self):
        board = Board()
        col1_cards = [Card(6, Suit.club, True)]
        col2_cards = [Card(10, Suit.club, True), Card(8, Suit.club, True), Card(7, Suit.club, True),
                      Card(6, Suit.club, True)]
        col3_cards = [Card(6, Suit.club, True)]
        col4_cards = [Card(5, Suit.club, True), Card(4, Suit.club, True)]
        col5_cards = [Card(2, Suit.club, True)]

        board.columns[1] = Column(col1_cards)
        board.columns[2] = Column(col2_cards)
        board.columns[3] = Column(col3_cards)
        board.columns[4] = Column(col4_cards)
        board.columns[5] = Column(col5_cards)

        self.game_engine.board = board
        best_col = self.game_engine.find_best_col_to_place(0, 4)
        self.assertEqual(best_col, 2)
        best_col = self.game_engine.find_best_col_to_place(0, 5)
        self.assertEqual(best_col, 5)

    def test_contains_complete_sequence(self):
        col1_cards = [Card(10, Suit.club, True), Card(8, Suit.club, True), Card(7, Suit.club, True),
                      Card(6, Suit.club, True)]
        column = Column(col1_cards)
        self.game_engine.board.columns[1] = column
        self.assertFalse(self.game_engine.contains_complete_sequence(1))

        col1_cards = [Card(i, Suit.club, True) for i in range(13, 0, -1)]
        column = Column(col1_cards)
        self.game_engine.board.columns[1] = column
        self.assertTrue(self.game_engine.contains_complete_sequence(1))

        col1_cards[4].revealed = False
        column = Column(col1_cards)
        self.game_engine.board.columns[1] = column
        self.assertFalse(self.game_engine.contains_complete_sequence(1))

    def test_move_to_blank_column(self):
        column1 = Column([])
        column2 = Column([Card(10, Suit.club, True), Card(8, Suit.club, True), Card(7, Suit.club, True)])

        board = Board()
        board.columns[1] = column1
        board.columns[2] = column2

        self.game_engine.board = board

        self.game_engine.move_cards(1, 2, 1)
        self.assertEquals(len(board.columns[1]), 2)

    def test_find_empty_column(self):
        column1 = Column([])
        column2 = Column([Card(13, Suit.club, True), Card(12, Suit.club, True), Card(11, Suit.club, True)])

        board = Board()
        board.columns[1] = column1
        board.columns[2] = column2

        self.game_engine.board = board

        self.assertEquals(self.game_engine.find_best_col_to_place(0, 2), 1)
