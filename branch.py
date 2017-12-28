import subprocess
import curses
import logging as log

def delete_branch(name):
    return subprocess.check_output(['git', 'branch', '-d', name])

def get_branches():
    return format_branches(get_git_branches())


def get_git_branches():
    return subprocess.check_output(['git', 'branch', '-lvv'])

def get_git_branch_names():
    return subprocess.check_output(['git', 'branch'])

def get_branch_names():
    return format_branches(get_git_branch_names())

def format_branches(blob):
    blob = str(blob)
    blob = blob[2:]
    newlines = blob.split('\\n')
    newlines = newlines[:-1]
    newlines = list(filter(lambda x: '*' not in x, newlines))
    newlines = trim_branches(newlines)
    newlines = list(filter(parse_branch_description, newlines))
    return newlines

def parse_branch_description(branch):
    tokens = branch.split(' ')
    if tokens[0] == 'master':
        return False
    return True

def trim_branches(branches):
    branches = list(map(lambda x: x[0:curses.COLS-2], branches))
    branches = list(map(remove_pad, branches))
    return branches

def remove_pad(branch):
    while branch[0] == ' ':
        branch = branch[1:]
    return branch

def get_branch_dimensions(branches):
    height = len(branches)
    lengths = list(map(lambda x: len(x), branches))
    width = max(lengths)
    return (height, width)
