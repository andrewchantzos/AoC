from aocd.models import Puzzle
import re
from utils import *

puzzle = Puzzle(year=2022, day=7)

inp = puzzle.input_data.splitlines()[2:]

# inp = """$ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k"""

# inp = inp.splitlines()[2:]

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

print(size)

total = 0
bad_sol = set()
for v, dir_size in size.items():
    if dir_size <= 100000:
        total += dir_size
        print(v, dir_size)

        bad_sol.add(v)

print(total)

from collections import defaultdict
from itertools import accumulate

val = list(map(str.split, puzzle.input_data.splitlines()))
dirs = defaultdict(int)
path = []

for v in val:
    if v[0] == "$":
        if v[1] == "cd":
            path.pop() if v[2] == ".." else path.append(v[2])
    elif v[0] != "dir":
        for p in accumulate(path, lambda x, y: x + "/" + y):
            dirs[p] += int(v[0])

# print([key for key, size in dirs.items() if size <= 100_000])
