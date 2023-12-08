from aocd.models import Puzzle
from src.utils import *
import math

puzzle = Puzzle(year=2023, day=8)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()


def read_input(inp):
    pattern = inp[0]
    d = {}
    for line in inp[2:]:
        parts = line.split("=")
        key = parts[0].strip()
        d[key] = tuple(part.strip("()").strip() for part in parts[1][1:].split(","))
    return pattern, d


pattern, d = read_input(inp)


def get_step(pos, endswith):
    step = 0
    while True:
        to_do = pattern[step % len(pattern)]
        step += 1
        next = d[pos][0] if (to_do == "L") else d[pos][1]
        pos = next
        if next.endswith(endswith):
            return step


puzzle.answer_a = get_step("AAA", "ZZZ")

# Part 2

starting_positions = [key for key in d if key.endswith("A")]

steps = [get_step(a, "Z") for a in starting_positions]

# Gather all steps and do least common multiple
puzzle.answer_b = math.lcm(*steps)
