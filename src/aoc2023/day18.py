from aocd.models import Puzzle
from src.utils import *
from shapely.geometry import Polygon
puzzle = Puzzle(year=2023, day=18)

inp = puzzle.input_data.splitlines()


def get_steps(part1=True):
    steps = []
    for line in inp:
        if part1:
            direc, length, _ = line.split(" ")
            length = int(length)
            steps.append((Direction[direc], length))
        else:
            last = line.split(" ")[-1]
            direc = Direction(int(last[-2]))
            length = int(last[-7:-2], 16)
            steps.append((direc, length))
    return steps


def solution(part1=True):
    perimeter = 0
    x, y = 0, 0
    coords = []
    for direc, length in get_steps(part1):
        coords.append((x, y))
        x, y = x + direc.diff()[0] * length, y + direc.diff()[1] * length
        perimeter += length
    # Pick's theorem
    # area = interior + perimeter / 2 - 1 
    # interior = area + 1 - perimeter / 2
    interior = int(Polygon(coords).area) - perimeter // 2 + 1
    return interior + perimeter

puzzle.answer_a = solution(True)
puzzle.answer_b = solution(False)
