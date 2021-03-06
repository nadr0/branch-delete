import curses
import menu
import logging as log
import branch

class Prompt(menu.Menu):

    def __init__(self, layout):
        super(Prompt, self).__init__(layout)
        self.options = ['Do you want to delete this branch?',' Yes',' No']
        self.write_options()

    def write_options(self):
        self.append_storage(self.options)

    def create_delete_copy(self, name):
        front = 'Do you want to delete '
        back =  '?'
        crop_length = curses.COLS - len(front) - len(back)
        name = name[0:crop_length]
        return front + name + back

    def generate_option_events(self, data):
        option_callbacks = [
            (self.noop, None),
            (self.wrapper, data),
            (self.close, None)
        ]
        return option_callbacks

    def open(self, name):
        self.selected_index = 1
        self.set_storage([
            self.create_delete_copy(name),
            ' Yes',
            ' No'
        ])
        self.draw()
        self.update()
        self.storage_event = []
        self.append_storage_event(self.generate_option_events(name))

    def close(self, *args):
        self.win.clear()
        self.update()
        return 'close'

    def eat_key(self, c):
        if  c == ord('j'):
            self.select('DOWN')
            pass
        elif c == ord('k'):
            self.select('UP')
            pass
        elif c == 10:
            result = self.select_event()
            return result

    def wrapper(self, data):
        branch.delete_branch(data)
        return 'deleted'

    def noop(self, *args):
        return None
