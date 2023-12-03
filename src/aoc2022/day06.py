from aocd.models import Puzzle
import re
from utils import *

puzzle = Puzzle(year=2022, day=6)

inp = puzzle.input_data.splitlines()

total = 0
for line in inp:
    for i in range(len(line)):
        if len(set(line[i:i+4])) == 4:
            total += (i + 4)
            break

puzzle.answer_a = total

total = 0
for line in inp:
    for i in range(len(line)):
        if len(set(line[i:i+14])) == 14:
            total += (i + 14)
            break

puzzle.answer_b = total