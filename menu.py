import curses
import math
import sys
import logging as log
from pprint import pformat

class Menu:

    DIRECTION_UP = 'UP'
    DIRECTION_DOWN = 'DOWN'

    def __init__(self, layout, border=True):
        self.win = curses.newwin(layout[0],
                                 layout[1],
                                 layout[2],
                                 layout[3])
        self.update()
        self.storage = []
        self.storage_event = []
        self.border = border
        # NOTE: Default setting
        self.selectable = False
        self.page_number = 1
        self.page_index = 0
        self.selected_index = 0
        self.draw_border()
        self.user_list = None
        self.buffered_line_count = 0
        # self.win.bkgd(' ', curses.color_pair(3))

    def set_user_list(self, user_list):
        self.user_list = user_list

    def update(self):
        self.win.refresh()

    def set_storage(self,data, index=None):
        if index:
            self.storage[index] = data
        else:
            self.storage = data

    def append_storage(self, data):
        self.storage.extend(data)

    def append_storage_event(self, events):
        self.storage_event.extend(events)

    def prepend_storage_event(self, events):
        self.storage_event = events + self.storage_event

    def prepend_storage(self, data):
        self.storage = data + self.storage

    def number_of_drawable_rows(self):
        return self.win.getmaxyx()[0]

    def clear(self):
        self.storage = []
        self.storage_event = []
        self.page_number = 1
        self.page_index = 0
        self.selected_index = 0
        self.buffered_line_count = 0
        self.win.clear()

    def draw_border(self):
        if self.border:
            self.win.border(0)

    def draw(self):
        self.win.clear()
        self.draw_border()
        self.write_storage()
        self.update()

    # TODO: Remove this at some point
    def write_clear(self):
        loc = self.draw_location()
        lines = self.page_length()
        blank_line = ' ' * self.draw_bounds()[1]
        for i in range(0, lines):
            draw_y = loc[0] + i
            draw_x = loc[1]
            if self.draw_inbounds(draw_y, draw_x):
                # TODO: Fix with try cache, because addstr \n places cursor, bottom right corner
                self.win.addstr(draw_y, draw_x, blank_line)

    def write_storage(self):
        loc = self.draw_location()
        lines = self.read_storage()
        local_selected = self.local_selected_index(self.selected_index);
        for i in range(0, len(lines)):
            draw_y = loc[0] + i
            draw_x = loc[1]
            line_to_draw = lines[i]
            line_width = self.draw_line_width()
            if len(line_to_draw) > line_width:
                line_to_draw = line_to_draw[0:line_width]

            if self.draw_inbounds(draw_y, draw_x):
                # TODO: Fix with try cache, because addstr \n places cursor, bottom right corner
                if i == local_selected and self.selectable:
                    self.win.addstr(draw_y, draw_x, line_to_draw, curses.color_pair(1))
                else:
                    self.win.addstr(draw_y, draw_x, line_to_draw)

    def local_selected_index(self, index):
        return abs(self.page_length() - ((self.page_length() * self.page_number)-self.selected_index))

    def read_storage(self):
        if self.page_number <= self.page_count():
            read = self.page_length() * self.page_number
            output = self.storage[self.page_index:read]
            return output
        return []

    def draw_location(self):
        if self.border:
            return (1,1)
        return (0,0)

    def draw_bounds(self):
        if self.border:
            y,x = self.win.getmaxyx()
            return (y - 2, x - 2)
        return self.win.getmaxyx()

    def draw_inbounds(self, y, x):
        b_y, b_x = self.draw_bounds()
        if y > b_y:
            return False
        if x > b_x:
            return False
        if y < 0:
            return False
        if x < 0:
            return False
        return True

    def draw_line_width(self):
        return self.draw_bounds()[1]

    def page_count(self):
        return math.ceil(len(self.storage)/self.draw_bounds()[0])

    def compute_page_count(self, lines):
        return math.ceil(len(lines)/self.draw_bounds()[0])

    def page_length(self):
        return self.draw_bounds()[0]

    def select_event(self):
        try :
            event = self.storage_event[self.selected_index]
            return event[0](event[1])
        except Exception as e:
            log.error(e)
            log.error('No Event Action off Select(enter)')

    def select_down(self):
        if self.selected_index < len(self.storage) - 1:
            self.selected_index = self.selected_index + 1
        if self.selected_index >= self.page_length() * self.page_number:
            self.scroll_down()

    def select_up(self):
        if self.selected_index > 0:
            self.selected_index = self.selected_index - 1
        if self.selected_index < self.page_length() * (self.page_number - 1):
            self.scroll_up()

    def select(self, direction):
        if direction == self.DIRECTION_UP:
            self.select_up()
        elif direction == self.DIRECTION_DOWN:
            self.select_down()

        self.write_clear()
        self.write_storage()
        self.update()

    def scroll_down(self):
        if self.page_number < self.page_count():
            self.page_index = self.page_index + self.page_length()
            self.selected_index = self.page_index
            self.page_number = self.page_number + 1

    def scroll_up(self):
        if self.page_number > 1:
            self.page_index = self.page_index - self.page_length()
            self.selected_index = self.page_index + self.page_length() - 1
            self.page_number = self.page_number - 1

    def scroll(self, direction):
        if direction == self.DIRECTION_UP:
            self.scroll_up()
        elif direction == self.DIRECTION_DOWN:
            self.scroll_down()

        self.draw()

    def scroll_to_bottom(self):
        self.page_index = self.page_length()
        self.selected_index = self.page_index
        self.page_number = self.page_count()
        self.draw()

    def focus(self):
        self.selectable = True
        self.draw()

    def defocus(self):
        self.selectable = False
        self.draw()

    def eat_key(self, c):
        if  c == ord('j'):
            self.select('DOWN')
            pass
        elif c == ord('k'):
            self.select('UP')
            pass
        elif c == 10:
            self.select_event()
            pass

    def buffer_lines(self, lines):
        number_of_pages = self.compute_page_count(lines)
        total_lines = number_of_pages * self.page_length()
        total_buffer = total_lines - len(lines)
        buffer = [' '] * total_buffer
        lines = buffer + lines
        return lines

    def scroll_to_last_page(self):
        self.page_index = self.page_length() * (self.page_count() - 1)
        self.selected_index = self.page_index
        self.page_number = self.page_count()

    def fake_window_scroll(self):
        self.clear_previous_scroll()
        page_length = self.page_length()
        line_count_in_window = len(self.read_storage())
        [self.prepend_storage([' ' * self.draw_line_width()]) for _ in range(page_length - line_count_in_window)]
        self.buffered_line_count = page_length - line_count_in_window

    def clear_previous_scroll(self):
        self.storage = self.storage[self.buffered_line_count:]
        self.buffered_line_count = 0
