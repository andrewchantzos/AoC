from aocd.models import Puzzle
from src.utils import *
from collections import defaultdict

puzzle = Puzzle(year=2023, day=15)


inp = puzzle.input_data.strip().split(",")


def get_hash(string):
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256
    return val


boxes = defaultdict(dict)

for line in inp:
    label = line.split("-")[0].split("=")[0]
    v = get_hash(label)

    if "-" in line:
        boxes[v].pop(label, None)
    elif "=" in line:
        boxes[v][label] = int(line.split("=")[1])

total_b = 0

for i, box in boxes.items():
    total_b += sum((i + 1) * j * focal for j, focal in enumerate(box.values(), start=1))

puzzle.answer_a = sum(get_hash(line) for line in inp)
puzzle.answer_b = total_b
