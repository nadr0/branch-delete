import curses
import sys
import logging as log

class Navigator():
    '''
    Navigator Controls the windows in the application
    It will switch between the applications windows with a set
    of keybinds.

    Similar to the nav mode in Vim
    '''
    NAV_MODE = 'NAV MODE'

    def __init__(self, layout, key_bindings, main_window):
        self.win = curses.newwin(layout[0],
                                 layout[1],
                                 layout[2],
                                 layout[3])
        self.key_eater = key_bindings['s']['window']
        self.key_eater.focus()
        self.key_binds = key_bindings
        self.win.keypad(True)
        self.first_time = True
        self.main_window = main_window

        # NOTE: Application Loop
        self.eating_keys()

    def eating_keys(self):
        while True:
            c = self.win.getch()

            # Send the key to another window
            if self.key_eater:
                result = self.key_eater.eat_key(c)
                if result == 'enter':
                    kb = self.key_binds['d']
                    self.key_eater = kb['window']
                    self.key_eater.focus()
                if result == 'close':
                    kb = self.key_binds['s']
                    self.key_eater = kb['window']
                    self.key_eater.focus()
                    self.draw_info()
                if result == 'deleted':
                    kb = self.key_binds['s']
                    self.key_eater = kb['window']
                    self.key_eater.update_from_delete()
                    self.key_eater.focus()
                    self.draw_info()
                if result == 'quit':
                    break;
                continue

    def draw_info(self):
        header = ' Press enter to delete a local branch'
        padding = curses.COLS - len(header)
        header = header + (' ' * padding)
        header = header[0:curses.COLS]
        self.main_window.addstr(0, 0, header)
        self.main_window.refresh()
