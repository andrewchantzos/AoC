from aocd.models import Puzzle
import re
from src.utils import *

puzzle = Puzzle(year=2023, day=5)

inp = puzzle.input_data.splitlines()

# inp = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4""".splitlines()

# Part 1


seeds = inp[0].replace("seeds: ", "").split(" ")

new_seeds = []

for i in range(0, len(seeds), 2):
    start = int(seeds[i])
    step = int(seeds[i + 1])
    new_seeds.append(range(start, start + step))


# Read input

data = {}

elements = []

element = ""
for x, line in enumerate(inp[1:]):
    nums = [(int(x), int(y), int(z)) for x, y, z in re.findall(r"(\d+) (\d+) (\d+)", line)]
    t = line.split("-")
    if len(t) > 1:
        element = t[0]
        data[element] = []
        elements.append(element)
    if not nums:
        continue
    data[element].append(nums[0])


# positions = []
# for start, step in new_seeds:
#     pos = int(seed)
#     seed = int(seed)
#     for element in elements:
#         mappings = d[element]
#         for start, dest, step in mappings:
#             if pos > start and pos < start + step:
#                 diff = pos - start
#                 pos = dest + diff
#                 break

#     positions.append(pos)

# print(min(res))


# print(positions)
# print(min(positions))
# puzzle.answer_a = min(positions)


def find_range_overlap(range1, range2):
    overlap_start = max(range1.start, range2.start)
    overlap_end = min(range1.stop, range2.stop)

    if overlap_start < overlap_end:
        return range(overlap_start, overlap_end)
    else:
        return None


range_stack = new_seeds

seen = set()
for element in elements:
    tmp_range = set()
    while range_stack:
        test_range = range_stack.pop()
        if test_range in seen:
            continue
        for dest, start, step in reversed(data[element]):
            new_range = range(start, start + step)
            overlap = find_range_overlap(test_range, new_range)
            if overlap:
                tmp_range.add(
                    range(dest - start + overlap.start, dest - start + overlap.start + len(overlap))
                )
                if len(overlap) != len(test_range):
                    if overlap.start > test_range.start:
                        range_stack.append(range(test_range.start, overlap.start))
                    if overlap.stop < test_range.stop:
                        range_stack.append(range(overlap.stop, test_range.stop))
                seen.add(test_range)
    range_stack = list(tmp_range)
    seen = set()


puzzle.answer_b = min([start.start for start in range_stack])
