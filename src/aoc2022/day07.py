from aocd.models import Puzzle
import re
from src.utils import *

puzzle = Puzzle(year=2022, day=7)

inp = puzzle.input_data.splitlines()[2:]


class Dir:
    def __init__(self, name, parent):
        self.parent = parent
        if parent:
            self.name = parent.name + "/" + name
        else:
            self.name = "/" + name
        self.files = []
        self.dirs = []

    def add_file(self, file):
        self.files.append(file)
    
    def add_dir(self, directory):
        self.dirs.append(directory)

    def get_size(self):
        size = sum(file[1] for file in self.files)
        for child in self.dirs:
            size += child.get_size()
        return size

directory = Dir("/", None)

parent = directory
for line in inp:
    if line.startswith("dir"):
        name = line.split(" ")[1]
        directory.add_dir(Dir(name, directory))
    elif line[0].isdigit():
        size, name = line.split(" ")
        directory.add_file((name, int(size)))
    elif line.startswith("$ cd .."):
        directory = directory.parent
    elif line.startswith("$ cd "):
        dir_name = (re.findall(r"\$ cd (\w+)", line))[0]
        if dir_name == "ctctt":
            pass
        for direc in directory.dirs:
            if direc.name.split("/")[-1] == dir_name:
                directory = direc
                break

size = {}

def get_sizes(directory):
    size[directory.name] = directory.get_size()
    for child in directory.dirs:
        get_sizes(child)

get_sizes(parent)

total = 0
for v, dir_size in size.items():
    if dir_size <= 100000:
        total += dir_size

puzzle.answer_a = total


missing_space = abs(40_000_000 - parent.get_size())

potential_deletions = [s for s in size.values() if s > missing_space]

puzzle.answer_b = min(potential_deletions)
