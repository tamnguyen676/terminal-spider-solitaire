from deck import Cards, Decks
from copy import deepcopy


class Column(Cards):
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        super().__init__(cards)

    def reveal_last(self):
        if len(self.cards) > 0:
            self.cards[-1].revealed = True

    def remove_cards(self, start_index):
        self.cards = self.cards[:start_index]
        self.reveal_last()


class Board:
    def __init__(self, show_suits=False):
        self.show_suits = show_suits
        self.deck = Decks(2, show_suits)

        self.completed = [False for _ in range(8)]
        self.columns = [Column() for _ in range(10)]
        self.stock = [Cards() for _ in range(5)]

        for stock in self.stock:
            for _ in range(10):
                stock.add_card(self.deck.pull_card())

        for i, column in enumerate(self.columns):
            num_cards = 6 if 1 <= i <= 4 else 5
            for _ in range(num_cards):
                column.add_card(self.deck.pull_card())
            column.reveal_last()

    def move_cards_to_completed(self, col_number):
        column = self.columns[col_number]
        column.remove_cards(len(column) - 13)
        for i in range(8):
            if not self.completed[i]:
                self.completed[i] = True
                break

    def move_card(self, row, from_col, to_col):
        source_column = self.columns[from_col]
        dest_column = self.columns[to_col]

        card = source_column[row]
        dest_column.add_card(card)
        del source_column[row]

    def deal_from_stock(self):
        if len(self.stock) > 0:
            stock = self.stock.pop()
            for i in range(1, 11):
                col_idx = i if i != 10 else 0
                card = stock.pull_card()
                self.columns[col_idx].add_card(card)
                self.columns[col_idx].reveal_last()

    def copy(self):
        board_copy = Board()
        board_copy.show_suits = self.show_suits
        board_copy.deck = deepcopy(self.deck)
        board_copy.completed = deepcopy(self.completed)
        board_copy.columns = deepcopy(self.columns)
        board_copy.stock = deepcopy(self.stock)
        return board_copy
