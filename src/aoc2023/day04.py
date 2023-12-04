from aocd.models import Puzzle
import re
from src.utils import *

puzzle = Puzzle(year=2023, day=4)

inp = puzzle.input_data.splitlines()



# Part 1

total = 0

def get_nums(string):
    nums = []
    for num in string.split(" "):
        if num != '':
            nums.append(int(num.strip()))
    return nums

d = {}
copies = {}
for x, line in enumerate(inp):
    part1, part2 = line.split(" | ")
    part1 = part1.split(":")[1].strip()
    part1 = get_nums(part1)
    part2 = get_nums(part2)

    length = len(set(part1) & set(part2)) 

    if length > 0:
        total += 2 ** (length - 1)

    d[x+1] = (part1, part2)
    copies[x+1] = 0

puzzle.answer_a = total

i = 1
for k, v in d.items():
    part1, part2 = v
    length = len(set(part1) & set(part2)) 
    for index in range(i + 1, i + 1 + length):
        copies[index] += copies[i] + 1

    copies[i] +=1
    i += 1

puzzle.answer_b = sum(copies.values())
