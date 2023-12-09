from email.policy import default
from aocd.models import Puzzle
from src.utils import *
from collections import defaultdict
import numpy as np
puzzle = Puzzle(year=2023, day=9)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()


total = 0
for history in inp:
    nums = defaultdict(list)
    nums[0] = [int(x) for x in history.split(" ")]

    step = 0
    while True:
        nums[step + 1] = [nums[step][i] - nums[step][i - 1] for i in range(1, len(nums[step]))]

        step += 1
        if all(x == 0 for x in nums[step]):
            last = nums[step][-1]
            for i in range(step, 0, -1):
                last = last + nums[i - 1][-1]
            total += last
            break


puzzle.answer_a = total

# Part 2

total = 0
for history in inp:
    nums = defaultdict(list)
    nums[0] = [int(x) for x in history.split(" ")]

    step = 0
    while True:
        nums[step + 1] = [nums[step][i] - nums[step][i - 1] for i in range(1, len(nums[step]))]
        step += 1
        if all(x == 0 for x in nums[step]):
            last = nums[step][0]
            for i in range(step, 0, -1):
                last = -last + nums[i - 1][0]
            total += last
            break

puzzle.answer_b = total
