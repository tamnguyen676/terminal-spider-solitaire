from src.board import Board
from src.deck import Card


class GameEngine:
    def __init__(self, suits):
        self.suits = suits
        self.board = Board(suits == 4)
        self.holding_cards = (None, None)
        self.previous_state = []
        self.score = 500

    def move_cards(self, row, from_col, to_col):
        source_column = self.board.columns[from_col]
        dest_column = self.board.columns[to_col]

        card = source_column[row]
        valid_transfer = len(dest_column) == 0 or dest_column[-1].equals(card, self.suits, offset=1)
        can_move_next_card = True

        if valid_transfer:
            self.previous_state.append(self.board.copy())
            self.score -= 1

        while valid_transfer and can_move_next_card:
            card = source_column[row]
            valid_transfer = len(dest_column) == 0 or dest_column[-1].equals(card, self.suits, offset=1)
            self.board.move_card(row, from_col, to_col)
            can_move_next_card = row < len(source_column) and card.equals(source_column[row], self.suits, offset=1)

        source_column.reveal_last()
        game_ended = self.board.move_cards_to_completed(to_col) if self.contains_complete_sequence(to_col) else False
        return game_ended

    def hold_cards(self, column_num, row_num):
        column = self.board.columns[column_num]
        card = column.cards[row_num]
        card.holding = True
        if row_num + 1 < len(column):
            new_card = column.cards[row_num + 1]
            if card.equals(new_card, self.suits, 1) and new_card.revealed:
                self.hold_cards(column_num, row_num + 1)

    def unhold_cards(self):
        for col in self.board.columns:
            for card in col:
                card.holding = False
        self.holding_cards = (None, None)

    def find_best_col_to_place(self, row_num, col_num):
        card = self.board.columns[col_num][row_num]
        empty_column_num = None
        consec_cards = [0 for _ in range(10)]
        for i, column in enumerate(self.board.columns):
            if len(column) == 0:
                empty_column_num = i
            j = len(column) - 1
            prev_card = card
            while j >= 0 and column[j].equals(prev_card, self.suits, offset=1):
                consec_cards[i] += 1
                prev_card = column[j]
                j -= 1

        if max(consec_cards) == 0:
            return col_num if empty_column_num is None else empty_column_num

        return max(range(10), key=lambda i: consec_cards[i])

    def find_best_row_idx(self, col_number):
        column = self.board.columns[col_number]
        if len(column) == 0:
            return 0

        idx = len(column) - 1
        best_idx = idx
        while idx > 0:
            card = column[idx]
            if card.revealed:
                prev_card = column[idx - 1]
                if prev_card.revealed and prev_card.equals(card, self.suits, 1):
                    best_idx = idx - 1
                else:
                    break

            idx -= 1

        return best_idx

    def contains_complete_sequence(self, col_number):
        column = self.board.columns[col_number]
        if len(column) >= 13 and column[-1].value == 1:

            ref_card = Card(0, column[-1].suit)
            val_to_check = 1
            for i in range(len(column) - 1, len(column) - 14, -1):
                if not column[i].equals(ref_card, self.suits, val_to_check) or not column[i].revealed:
                    return False
                val_to_check += 1
            self.score += 100
            return True
        else:
            return False

    def can_hold(self, row_num, col_num):
        column = self.board.columns[col_num]

        if row_num == len(column) - 1:
            return True

        while row_num < len(column) - 1:
            if not column[row_num].equals(column[row_num + 1], self.suits, 1):
                return False
            row_num += 1

        return True

    def deal_new_cards(self):
        self.previous_state.append(self.board.copy())
        self.board.deal_from_stock()

    def undo(self):
        self.board = self.previous_state.pop()
        self.score -= 1
        self.unhold_cards()

# BUG Not pinned very well
# Crashed if column too long