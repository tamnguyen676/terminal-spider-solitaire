from src.screen_interface import ScreenInterface
import curses
import sys

class MainMenu(ScreenInterface):
    def __init__(self, screen, min_rows, min_cols):
        super().__init__(screen, min_rows, min_cols)

    def print_large_title(self):
        title = \
'''                                                                        ________
 _____       _     _             _____       _   _        _            |        |
/  ___|     (_)   | |           /  ___|     | (_) |      (_)           | ||  || |
\ `--. _ __  _  __| | ___ _ __  \ `--.  ___ | |_| |_ __ _ _ _ __ ___   | \\\\()// |
 `--. \ '_ \| |/ _` |/ _ \ '__|  `--. \/ _ \| | | __/ _` | | '__/ _ \\  |//(__)\\\\|
/\__/ / |_) | | (_| |  __/ |    /\__/ / (_) | | | || (_| | | | |  __/  |||    |||
\____/| .__/|_|\__,_|\___|_|    \____/ \___/|_|_|\__\__,_|_|_|  \___|  |________|
      | |                                                            
      |_| '''.split('\n')
        width = self.num_cols
        mid_str = len(title[0]) // 2
        spaces = ' ' * int(width / 2 - mid_str)
        for i, line in enumerate(title):
            to_print = spaces + line + '\n' if i != len(line) - 1 else ''
            self.screen.addstr(to_print, curses.color_pair(3))

    def print_small_title(self):
        title = \
'''  ___      _    _           ___      _ _ _        _         
 / __|_ __(_)__| |___ _ _  / __| ___| (_) |_ __ _(_)_ _ ___ 
 \__ \ '_ \ / _` / -_) '_| \__ \/ _ \ | |  _/ _` | | '_/ -_)
 |___/ .__/_\__,_\___|_|   |___/\___/_|_|\__\__,_|_|_| \___|
     |_| '''.split('\n')
        width = self.num_cols
        mid_str = len(title[0]) // 2
        spaces = ' ' * int(width / 2 - mid_str)
        for i, line in enumerate(title):
            to_print = spaces + line + '\n' if i != len(line) - 1 else ''
            self.screen.addstr(to_print, curses.color_pair(3))

    def show_main_menu(self):
        self.screen.clear()
        self.force_screen_size(self.min_rows, self.min_cols)
        if self.num_rows > 20:
            self.print_large_title()
            self.print_horizontally_centered('[1] Play 1 Suit\n\n')
            self.print_horizontally_centered('[2] Play 2 Suit\n\n')
            self.print_horizontally_centered('[3] Play 4 Suit\n\n')
        else:
            self.print_small_title()
            self.print_horizontally_centered('[1] Play 1 Suit\n')
            self.print_horizontally_centered('[2] Play 2 Suit\n')
            self.print_horizontally_centered('[3] Play 4 Suit\n')
        self.print_horizontally_centered('[Q] Quit\n\n')
        self.print_horizontally_centered('Developed by Tam Nguyen\n')
        self.print_horizontally_centered('https://www.linkedin.com/in/tamnguyen676/\n')
        self.print_horizontally_centered('Buy dev a coffee ☺  - https://www.buymeacoffee.com/tamnguyen\n')

        self.screen.refresh()

    def wait_for_input(self):
        try:
            keycode = self.screen.getch()

            if keycode == curses.KEY_RESIZE:
                self.num_rows, self.num_cols = self.screen.getmaxyx()

            char = chr(keycode)

            if char == '1':
                return 1
            elif char == '2':
                return 2
            elif char == '3' or char == '4':
                return 4
            elif char == 'q' or char == 'Q':
                curses.endwin()
                sys.exit()
        except ValueError:
            pass
