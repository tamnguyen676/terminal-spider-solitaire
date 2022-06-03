from screen_interface import ScreenInterface
import curses


class GUI(ScreenInterface):
    def __init__(self, game_engine, screen, min_rows, min_cols):
        super().__init__(screen, min_rows, min_cols)

        self.game_engine = game_engine

        self.cursor_col = 1
        self.cursor_row = 5
        self.padding = 6 if game_engine.suits != 4 else 7

        self.cyan = curses.color_pair(1)
        self.red = curses.color_pair(2)
        self.green = curses.color_pair(3)

        self.column_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    def _print_tableau(self):
        for i in range(1, 11):
            col_idx = i if i != 10 else 0
            column = self.game_engine.board.columns[col_idx]

            if len(column) == 0:
                x = self.padding * (i - 1) + self.padding - 1
                if self.cursor_col != col_idx:
                    self.screen.addstr(4, x, '_')
                else:
                    self.screen.addstr(4, x - 3, '-> _')

            for row_num, card in enumerate(column):

                symbol = card.symbol if card.revealed else '*'
                x = self.padding * (i - 1) + self.padding - len(symbol)

                if row_num == self.cursor_row and col_idx == self.cursor_col:
                    self.screen.addstr(4 + row_num, x - 3, '-> ')

                if card.holding:
                    x -= 1

                if self.game_engine.suits != 1 and card.is_red and card.revealed:
                    self.screen.addstr(4 + row_num, x, symbol, self.red)
                else:
                    self.screen.addstr(4 + row_num, x, symbol)

    def _move_cursor_vertical(self, up):

        column = self.game_engine.board.columns[self.cursor_col]

        if len(column) > 0:
            moved_cursor_row = self.cursor_row - up
            first_revealed_row = next(filter(lambda i: column[i].revealed, range(len(column))))

            if moved_cursor_row == first_revealed_row - 1:
                moved_cursor_row = len(column) - 1
            elif moved_cursor_row == len(column):
                moved_cursor_row = first_revealed_row

            if column[moved_cursor_row].revealed:
                self.cursor_row = moved_cursor_row
                self.show_board()

    def _move_cursor_horizontal(self, right):
        moved_cursor_col = self.cursor_col + right
        if moved_cursor_col == 10:
            moved_cursor_col = 0
        elif moved_cursor_col == -1:
            moved_cursor_col = 9
        self.cursor_row = self.game_engine.find_best_row_idx(moved_cursor_col)
        self.cursor_col = moved_cursor_col
        self.show_board()

    def _print_first_row(self):
        self.screen.addstr('\n')
        self.screen.addstr(' ' * (self.padding - 1))
        num_stock = len(self.game_engine.board.stock)

        for _ in self.game_engine.board.stock:
            self.screen.addstr('*', curses.A_STANDOUT)
            self.screen.addstr(' ')

        self.screen.addstr('  ' * (5 - num_stock))

        num_spaces = self.padding * 10 - self.padding + 1 - 10 - 15
        self.screen.addstr(" " * num_spaces)

        for completed in self.game_engine.board.completed:
            if completed:
                self.screen.addstr('K', curses.A_STANDOUT | curses.A_UNDERLINE)
            else:
                self.screen.addstr(' ', curses.A_UNDERLINE)
            self.screen.addstr(' ')

        self.screen.addstr('\n\n')

    def _print_side_bar(self):
        x = self.padding * 10 + 5
        self.screen.addstr(1, x, f'Score: ')
        self.screen.addstr(str(self.game_engine.score), self.green)
        self.screen.addstr(3, x, '[Space/Enter] Select')
        self.screen.addstr(5, x, '[n] Deal new cards')
        self.screen.addstr(7, x, '[u] Undo')
        self.screen.addstr(9, x, '[i] Info')
        self.screen.addstr(11, x, '[q] Main Menu')

    def _print_info(self):
        strings = ['To navigate and move the cursor, use the arrow keys.',
                   'Vim bindings are also valid (h,j,k,l)',
                   'You can also press the number of the column to jump to that column.\n',
                   'Press enter or space to select cards. Press it again to instantly place it in the',
                   'best column if one is available. You can also press the number of',
                   'the column you want to specifically move it to or you can move the',
                   'cursor to a column and press enter/space to drop it in that column.\n',
                   'Press u or backspace to undo a move or a selection',
                   'Press n to deal new cards',
                   'Press q (while in game) to return back to the main menu\n',
                   'For every move and every move you undo, 1 point is lost.',
                   'Every suit completed, 100 points are gained. The max score is 1254.\n',
                   'For game info and rules: https://en.wikipedia.org/wiki/Spider_(solitaire)\n',
                   'PRESS Q TO RETURN TO GAME'
                   ]
        self.print_centered(strings, bold_last=True)

    def show_board(self):
        self.screen.erase()
        rows_to_display = len(max(self.game_engine.board.columns, key=lambda column: len(column))) + 5
        if rows_to_display > self.num_rows:
            self.force_screen_size(rows_to_display, self.min_cols)
        self._print_first_row()
        self.screen.addstr(''.join(map(lambda num: str(num).rjust(self.padding), self.column_numbers)), self.cyan)
        self.screen.addstr('\n')
        self._print_tableau()
        self._print_side_bar()

        self.screen.refresh()

    def move_cursor_up(self):
        self._move_cursor_vertical(up=1)

    def move_cursor_down(self):
        self._move_cursor_vertical(up=-1)

    def move_cursor_right(self):
        self._move_cursor_horizontal(right=1)

    def move_cursor_left(self):
        self._move_cursor_horizontal(right=-1)

    def move_cursor_to_column(self, col_num):
        self.cursor_col = col_num
        self.cursor_row = self.game_engine.find_best_row_idx(col_num)
        self.show_board()

    def main_loop(self):
        self.show_board()
        while True:
            keycode = self.screen.getch()
            if keycode == curses.KEY_RESIZE:
                self._handle_resize(self.show_board)

            try:
                char = chr(keycode)

                if keycode == curses.KEY_UP or char.lower() == 'k':
                    self.move_cursor_up()
                elif keycode == curses.KEY_RIGHT or char.lower() == 'l':
                    self.move_cursor_right()
                elif keycode == curses.KEY_DOWN or char.lower() == 'j':
                    self.move_cursor_down()
                elif keycode == curses.KEY_LEFT or char.lower() == 'h':
                    self.move_cursor_left()
                elif keycode == 10 or char.lower() == ' ':  # Enter or Space
                    if self.game_engine.holding_cards == (None, None):
                        if len(self.game_engine.board.columns[self.cursor_col]) > 0:
                            if self.game_engine.can_hold(self.cursor_row, self.cursor_col):
                                self.game_engine.holding_cards = (self.cursor_row, self.cursor_col)
                                self.game_engine.hold_cards(self.cursor_col, self.cursor_row)
                    else:
                        holding_row, holding_col = self.game_engine.holding_cards
                        if self.game_engine.holding_cards[1] == self.cursor_col:
                            dest_col_num = self.game_engine.find_best_col_to_place(holding_row, holding_col)
                        else:
                            dest_col_num = self.cursor_col
                        game_ended = self._move_cards(holding_row, holding_col, dest_col_num)
                        if game_ended:
                            return

                    self.show_board()
                elif 48 <= keycode <= 57:
                    col_num = int(char)
                    if self.game_engine.holding_cards == (None, None):
                        self.move_cursor_to_column(col_num)
                    else:
                        row, from_col = self.game_engine.holding_cards
                        game_ended = self._move_cards(row, from_col, col_num)
                        if game_ended:
                            return
                elif char.lower() == 'n':
                    self.game_engine.deal_new_cards()
                    self.show_board()
                elif char.lower() == 'u' or keycode == curses.KEY_BACKSPACE:
                    if self.game_engine.holding_cards != (None, None):
                        self.game_engine.unhold_cards()
                    elif len(self.game_engine.previous_state) > 0:
                        self.game_engine.undo()
                    self.show_board()
                elif char.lower() == 'i':
                    self._print_info()
                    while True:
                        keycode = self.screen.getch()
                        if keycode == curses.KEY_RESIZE:
                            self._handle_resize(self._print_info)
                        try:
                            if chr(keycode).lower() == 'q':
                                self.screen.erase()
                                self.show_board()
                                break
                        except:
                            pass
                elif char.lower() == 'q':
                    self.screen.erase()
                    return
            except ValueError:
                pass

    def _handle_resize(self, func_after_resize):
        self.num_rows, self.num_cols = self.screen.getmaxyx()
        if self.num_cols < self.min_cols or self.num_rows < self.min_rows:
            self.force_screen_size(self.min_rows, self.min_cols)
        func_after_resize()

    def _move_cards(self, row, from_col_num, to_col_num):
        game_ended = self.game_engine.move_cards(row, from_col_num, to_col_num)
        self.game_engine.unhold_cards()
        self.cursor_col = to_col_num
        self.cursor_row = self.game_engine.find_best_row_idx(to_col_num)
        self.show_board()
        if game_ended:
            curses.napms(250)
            self.print_centered(['You Win!\n', f'Score: {self.game_engine.score}\n', 'Press Q to Return to Menu'])
            while True:
                keycode = self.screen.getch()
                if keycode == curses.KEY_RESIZE:
                    self._handle_resize(self._print_info)
                try:
                    if chr(keycode).lower() == 'q':
                        self.screen.erase()
                        break
                except:
                    pass
        return game_ended
