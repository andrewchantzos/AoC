from aocd.models import Puzzle
import re

puzzle = Puzzle(year=2022, day=4)

inp = puzzle.input_data.splitlines()


def total_overlap(t1, t2):
    start1, end1 = t1
    start2, end2 = t2

    return start1 <= start2 and end1 >= end2 or start2 <= start1 and end2 >= end1


def partial_overlap(t1, t2):
    start1, end1 = t1
    start2, end2 = t2

    return end1 >= start2 and end2 >= start1


total_overlaps = 0

for line in inp:
    windows = [(int(x), int(y)) for x, y in re.findall(r"(\d+)-(\d+)", line)]
    w1, w2 = windows[:2]
    total_overlaps += total_overlap(w1, w2)

puzzle.answer_a = total_overlaps

partial_overlaps = 0
for line in inp:
    windows = [(int(x), int(y)) for x, y in re.findall(r"(\d+)-(\d+)", line)]
    w1, w2 = windows[:2]
    partial_overlaps += partial_overlap(w1, w2)

puzzle.answer_b = partial_overlaps
