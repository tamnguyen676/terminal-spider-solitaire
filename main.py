from src.game_engine import GameEngine
from src.gui import GUI
from src.main_menu import MainMenu
import curses

curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_CYAN, -1)
curses.init_pair(2, curses.COLOR_RED, -1)
curses.init_pair(3, curses.COLOR_GREEN, -1)
curses.curs_set(0)


def start(screen):
    menu = MainMenu(screen, 17, 85)
    screen.scrollok(1)
    while True:
        menu.show_main_menu()
        suits_to_use = menu.wait_for_input()
        if suits_to_use in {1, 2, 4}:
            min_cols = 85 if suits_to_use != 4 else 95
            graphics = GUI(GameEngine(suits=suits_to_use), screen, 17, min_cols)
            screen.clear()
            screen.refresh()
            graphics.main_loop()


curses.wrapper(start)

# TODO
# Allow moving held cards with arrow
# Display instructions and points