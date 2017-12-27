import sys
import os
import curses
import logging as log
import navigator
import listing
import branch
import prompt

def main(stdscr):
    branch_data = branch.get_branches()
    branch_names = branch.get_branch_names()
    (height, width) = branch.get_branch_dimensions(branch_data)

    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    border_bounds = 2
    branch_layout = (curses.LINES - 1, curses.COLS, 1, 0)
    # 1 for the nav height itself
    nav_layout = (1, 1, curses.LINES, 0)

    prompt_layout = (5, curses.COLS, 0, 0)
    prompt_option = prompt.Prompt(prompt_layout)

    # Layout is (height, width, y_coord, x_coord)
    branch_list = listing.Listing(branch_layout, branch_data, branch_names)
    branch_list.set_prompt(prompt_option)

    stdscr.addstr(0, 0, ' Press enter to delete a local branch')
    stdscr.refresh()

    # Nav
    nav = navigator.Navigator(nav_layout,{
        's':{
            'window':branch_list
        },
        'd': {
            'window':prompt_option
        }
    }, stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
