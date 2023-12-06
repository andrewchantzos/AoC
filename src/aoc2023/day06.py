from aocd.models import Puzzle
import re
from src.utils import *

puzzle = Puzzle(year=2023, day=6)

inp = puzzle.input_data.splitlines()

# Part 1
time_ints = [int(match) for match in re.findall(r"\b\d+\b", inp[0])]
dist_ints = [int(match) for match in re.findall(r"\b\d+\b", inp[1])]

pairs = zip(time_ints, dist_ints)

res = 1
for t, d in pairs:
    for i in range(t):
        if i * (t - i) > d:
            res *= len(range(i, t - i + 1))
            break

puzzle.answer_a = res


# part two

t = int(inp[0].replace("Time:", "").replace(" ", ""))
d = int(inp[1].replace("Distance:", "").replace(" ", ""))

for i in range(t):
    if i * (t - i) > d:
        res = len(range(i, t - i + 1))
        puzzle.answer_b = res
        break
