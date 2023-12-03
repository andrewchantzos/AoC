from aocd.models import Puzzle
import re
from src.utils import *

puzzle = Puzzle(year=2023, day=3)
inp = puzzle.input_data.splitlines()

grid = Grid(inp)

total_a = 0

store_nums = []
for line_num, line in enumerate(inp):
    res = re.finditer(r"([0-9]+)", line)
    for num in res:
        start, end = num.span()
        num = int(num.group(0))
        store_nums.append((start, end, line_num, num))
        neighbours = grid.get_range_neighbours(line_num, start, end)

        if not all(grid[(x, y)] == '.' or grid[(x, y)].isdigit() for x, y in neighbours):
            total_a += num

puzzle.answer_a = total_a

# Part two
store_gears = []
for row, line in enumerate(inp):
    line = line.strip()
    for col, char in enumerate(line):
        if char == '*':
            store_gears.append((row, col))


# Find adjacent
total_b = 0
for gear_line, gear_pos in store_gears:
    nums = []
    for start, end, line, num in store_nums:
        # Above or below
        if (gear_line == line - 1 or gear_line == line + 1) and gear_pos >= start - 1 and gear_pos <= end:
            nums.append(num)
        # Same line
        if gear_line == line and (gear_pos == start - 1 or gear_pos == end):
            nums.append(num)
    if len(nums) == 2:
        total_b += nums[0]* nums[1]

puzzle.answer_b = total_b
