#!/usr/bin/env python3

from game_engine import GameEngine
from gui import GUI
from main_menu import MainMenu
import curses

curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_CYAN, -1)
curses.init_pair(2, curses.COLOR_RED, -1)
curses.init_pair(3, curses.COLOR_GREEN, -1)
curses.curs_set(0)

MIN_ROWS = 14
MIN_COLS = 85


def start(screen):
    screen.scrollok(True)
    screen.idcok(False)
    screen.idlok(False)

    menu = MainMenu(screen, MIN_ROWS, MIN_COLS)

    while True:
        menu.show_main_menu()
        suits_to_use = menu.wait_for_input()
        if suits_to_use in {1, 2, 4}:
            min_cols = MIN_COLS if suits_to_use != 4 else MIN_COLS + 10
            graphics = GUI(GameEngine(suits=suits_to_use), screen, MIN_ROWS, min_cols)
            screen.erase()
            screen.refresh()
            graphics.main_loop()


curses.wrapper(start)
