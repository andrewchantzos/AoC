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

seeds = [int(x) for x in inp[0].replace("seeds: ", "").split(" ")]

new_seeds = []
for i in range(0, len(seeds), 2):
    start = seeds[i]
    step = seeds[i + 1]
    new_seeds.append(range(start, start + step))


# Read input

data = {}

element = ""
for x, line in enumerate(inp[1:]):
    nums = [(int(x), int(y), int(z)) for x, y, z in re.findall(r"(\d+) (\d+) (\d+)", line)]
    if nums:
        data[element].append(nums[0])
    else:
        t = line.split("-")
        if len(t) > 1:
            element = t[0]
            data[element] = []


positions = []
for seed in seeds:
    pos = seed
    for element, mappings in data.items():
        for dest, start, step in mappings:
            if pos > start and pos < start + step:
                diff = pos - start
                pos = dest + diff
                break
    positions.append(pos)

puzzle.answer_a = min(positions)


# Part two


def find_range_overlap(range1, range2):
    """
    Will return the overlap between two ranges
    """
    overlap_start = max(range1.start, range2.start)
    overlap_end = min(range1.stop, range2.stop)

    if overlap_start < overlap_end:
        return range(overlap_start, overlap_end)
    return None


def get_leftover_ranges(main_range, overlap_range):
    """
    >>> list(get_leftover_ranges(range(1, 10), range(4,5)))
    >>> [range(1,4), range(5, 10)]
    """
    if overlap_range.start > main_range.start:
        yield range(main_range.start, overlap_range.start)
    if overlap_range.stop < main_range.stop:
        yield range(overlap_range.stop, main_range.stop)


range_stack = new_seeds

seen = set()
# For each level iterate over all the ranges
for element, element_ranges in data.items():
    level_ranges = set()
    while range_stack:
        seed_range = range_stack.pop()
        if seed_range in seen:
            # This is not needed, but it makes the code faster
            continue
        for dest, start, step in reversed(element_ranges):
            element_rng = range(start, start + step)
            if overlap := find_range_overlap(seed_range, element_rng):
                # Diff from the start and the start of the overlap
                diff = overlap.start - start
                level_ranges.add(range(dest + diff, dest + diff + len(overlap)))

                # Got leftover ranges to add
                # If there are parts of the range that do not match with the overlap
                # we need to carry them over
                range_stack.extend(get_leftover_ranges(seed_range, overlap))

                seen.add(seed_range)
    # Reset for next stage
    range_stack = list(level_ranges)
    seen = set()


puzzle.answer_b = min((start.start for start in range_stack))
