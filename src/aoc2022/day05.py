from aocd.models import Puzzle
import re
from utils import *

puzzle = Puzzle(year=2022, day=5)

inp = puzzle.input_data


part1 = inp.split("\n\n")[0].split("\n")
part2 = inp.split("\n\n")[1].split("\n")

grid = Grid(part1)

stacks = {}
i = 0
for col, char in enumerate(grid.grid[-1]):
    if (char.isdigit()):
        i += 1
        stacks[i] = [x for x in grid.get_column(col) if x.isalpha()]


for line in part2:
    windows = [(int(x), int(y), int(z)) for x, y, z in re.findall(r"move (\d+) from (\d+) to (\d+)", line)]
    el, frm, to = windows[0]
    from_list = stacks[frm]
    to_list = stacks[to]
    for _ in range(el):
        el = from_list.pop(0)
        if el:
            to_list.insert(0, el)

res = "".join(value[0] for value in stacks.values() if value)


puzzle.answer_a = res


# Part two
stacks = {}
i = 0
for col, char in enumerate(grid.grid[-1]):
    if (char.isdigit()):
        i += 1
        stacks[i] = [x for x in grid.get_column(col) if x.isalpha()]


for line in part2:
    windows = [(int(x), int(y), int(z)) for x, y, z in re.findall(r"move (\d+) from (\d+) to (\d+)", line)]
    el, frm, to = windows[0]
    from_list = stacks[frm]
    to_list = stacks[to]
    tmp_lst = []
    for _ in range(el):
        try:
            el = from_list.pop(0)
            if el:
                tmp_lst.append(el)
        except IndexError:
            pass 
    stacks[to] = tmp_lst + to_list

res = "".join(value[0] for value in stacks.values() if value)

puzzle.answer_b = res
