from aocd.models import Puzzle
from src.utils import *

puzzle = Puzzle(year=2022, day=1)

breakpoint()
inp = puzzle.input_data.splitlines()

# Part 1

def get_sum(inp):
    digits = ["".join(char for char in x if char.isdigit()) for x in inp]
    return sum([(int(x[0]) * 10 + int(x[-1])) for x in digits])


puzzle.answer_a = get_sum(inp)


# Part 2
numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

filtered_input = []
for line in inp:
    for k, v in numbers.items():
        line = line.replace(k, k + v + k)
    filtered_input.append(line)


puzzle.answer_b = get_sum(filtered_input)
