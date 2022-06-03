from board import Board
from deck import Card


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

        original_card = source_column[row]
        valid_transfer = len(dest_column) == 0 or dest_column[-1].equals(original_card, suits=1, offset=1)
        can_move_next_card = True

        if valid_transfer:
            self.previous_state.append(self.board.copy())
            self.score -= 1

        while valid_transfer and can_move_next_card:
            card = source_column[row]
            suits = 1 if card == original_card else self.suits
            valid_transfer = len(dest_column) == 0 or dest_column[-1].equals(card, suits, offset=1)
            self.board.move_card(row, from_col, to_col)
            can_move_next_card = row < len(source_column) and card.equals(source_column[row], self.suits, offset=1)

        source_column.reveal_last()
        self.check_for_completed_sequence(to_col)
        return self.has_game_ended()

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
        priorities = [(1, 0) for _ in range(10)]

        for i, column in enumerate(self.board.columns):
            if i == col_num:
                continue

            if len(column) == 0:
                empty_column_num = i
                continue

            j = len(column) - 1
            prev_card = card
            while j >= 0:
                first_move = j == len(column) - 1
                suits = 1 if first_move else self.suits
                valid_transfer = column[j].equals(prev_card, suits, offset=1)
                if valid_transfer:
                    if first_move:
                        priority = self._find_priority_best_col(column[j], prev_card)
                        priorities[i] = (priority, 0)
                    priorities[i] = priorities[i][0], priorities[i][1] + 1
                    prev_card = column[j]
                    j -= 1
                else:
                    break

        highest_priority_col = self._find_highest_priority_best_col(priorities)

        if highest_priority_col is None:
            return col_num if empty_column_num is None else empty_column_num

        return highest_priority_col

    def _find_priority_best_col(self, card, prev_card):
        if self.suits == 1:
            return 1

        same_color = card.is_red == prev_card.is_red
        if self.suits == 2:
            return 2 if same_color else 1

        same_suit = card.suit == prev_card.suit
        return 4 if same_suit else 2 if same_color else 1

    def _find_highest_priority_best_col(self, priorities):
        if all(tup[1] == 0 for tup in priorities):
            return None

        if self.suits == 1:
            return max(range(10), key=lambda i: priorities[i][1])

        same_suit_cards = []
        same_color_cards = []
        other_cards = []
        for i in range(10):
            if priorities[i][0] == 4:
                same_suit_cards.append((i, priorities[i][1]))
            elif priorities[i][0] == 2:
                same_color_cards.append((i, priorities[i][1]))
            else:
                other_cards.append((i, priorities[i][1]))
        if len(same_suit_cards) > 0:
            return max(same_suit_cards, key=lambda tup: tup[1])[0]
        elif len(same_color_cards) > 0:
            return max(same_color_cards, key=lambda tup: tup[1])[0]
        elif len(other_cards) > 0:
            return max(other_cards, key=lambda tup: tup[1])[0]
        else:
            return None

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

    def has_game_ended(self):
        return all(self.board.completed)

    def check_for_completed_sequence(self, col_number):
        column = self.board.columns[col_number]
        if len(column) >= 13 and column[-1].value == 1:

            ref_card = Card(0, column[-1].suit)
            val_to_check = 1
            for i in range(len(column) - 1, len(column) - 14, -1):
                if not column[i].equals(ref_card, self.suits, val_to_check) or not column[i].revealed:
                    return
                val_to_check += 1
            self.score += 100
            self.board.move_cards_to_completed(col_number)

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
        for i in range(len(self.board.columns)):
            self.check_for_completed_sequence(i)

    def undo(self):
        self.board = self.previous_state.pop()
        self.score -= 1
        self.unhold_cards()
