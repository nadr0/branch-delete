import curses
import menu
import logging as log
import branch

class Listing(menu.Menu):

    def __init__(self, layout, branches, branch_names):
        super(Listing, self).__init__(layout)
        self.branch_data = branches
        self.prompt = None
        self.branch_names = branch_names
        self.row_storage_index = 0
        self.write_branch_list()
        self.draw()
        self.update()

    def set_prompt(self, prompt):
        self.prompt = prompt
        self.set_branch_events(self.branch_names)

    def set_branch_events(self, data):
        branch_events = self.generate_branch_events(data)
        self.append_storage_event(branch_events)

    def set_branch_list(self, data):
        self.branch_data = data

    def write_branch_list(self):
        self.set_storage(self.branch_data)

    def generate_branch_events(self, data):
        branch_names = data;
        branch_callbacks = list(map(lambda x: self.prompt.open, data))
        return list(zip(branch_callbacks, branch_names))

    def update_listing(self):
        branch_data = branch.get_branches()
        branch_names = branch.get_branch_names()
        self.win.clear()
        self.branch_data = branch_data
        self.branch_names = branch_names
        self.write_branch_list()
        self.set_branch_events(self.branch_names)
        self.selected_index = 0
        self.draw()
        self.update()

    def focus(self):
        self.selectable = True
        self.storage = []
        self.storage_event = []
        self.update_listing()

    def eat_key(self, c):
        if  c == ord('j'):
            self.select('DOWN')
            pass
        elif c == ord('k'):
            self.select('UP')
            pass
        elif c == 10:
            self.select_event()
            return 'enter'
