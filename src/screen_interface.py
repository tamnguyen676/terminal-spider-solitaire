import curses
import sys


class ScreenInterface:
    def __init__(self, screen, min_rows, min_cols):
        screen.erase()
        self.screen = screen
        self.num_rows, self.num_cols = screen.getmaxyx()
        self.min_rows = min_rows
        self.min_cols = min_cols
        self.force_screen_size(min_rows, min_cols)

    def print_horizontally_centered(self, str, color=None):
        width = self.num_cols
        mid_str = len(str) // 2
        num_spaces = int(width / 2 - mid_str)
        spaces = ' ' * num_spaces
        if color is None:
            self.screen.addstr(spaces + str)
        else:
            self.screen.addstr(spaces + str, color)

    def _print_new_lines_to_center(self, num_lines):
        num_new_lines = (self.num_rows - num_lines) // 2
        self.screen.addstr('\n' * num_new_lines)

    def print_centered(self, strings, bold_last=False):
        self.screen.erase()
        num_lines = len(strings) + sum(map(lambda s: s[-1] == '\n', strings))
        self._print_new_lines_to_center(num_lines)
        for i, string in enumerate(strings):
            if bold_last and i == len(strings) - 1:
                self.print_horizontally_centered(string, curses.A_BOLD)
            else:
                self.print_horizontally_centered(string + '\n')

    def force_screen_size(self, min_rows, min_cols):
        while self.num_rows < min_rows or self.num_cols < min_cols:
            self.screen.erase()
            strings = [f'Please increase your window size to at least {min_cols}x{min_rows}',
                       f'Current size: {self.num_cols} x {self.num_rows}']
            self.print_centered(strings)
            key = self.screen.getch()
            if key == curses.KEY_RESIZE:
                self.num_rows, self.num_cols = self.screen.getmaxyx()
            elif chr(key) == 'q':
                sys.exit()
        self.screen.erase()
