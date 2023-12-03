from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day=3)

inp = puzzle.input_data.splitlines()

# inp = """vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()

# Part 1

def split_string_in_half(input_string):
    midpoint = len(input_string) // 2
    return input_string[:midpoint], input_string[midpoint:]

def get_val(char):
    if char.isupper():
        return ord(char) - ord('A') + 27
    return ord(char) - ord('a') + 1

from itertools import chain

answer_a = 0
for line in inp:
    first, second = split_string_in_half(line)
    for el in list(set(first) & set(second)):
        answer_a += get_val(el)

puzzle.answer_a = answer_a


answer_b = 0

# Iterate over lines in groups of three
for i in range(0, len(inp), 3):
    first, second, third = inp[i:i+3]

    # Process or print the group of three lines
    for el in (list(set(first) & set(second) & set(third))):
        answer_b += get_val(el)

puzzle.answer_b = answer_b
