from aocd.models import Puzzle
from src.utils import *
from collections import namedtuple, defaultdict


puzzle = Puzzle(year=2023, day=22)

inp = puzzle.input_data.splitlines()
# inp = puzzle.example_data.splitlines()


Cube = namedtuple("Cube", ["x", "y", "z"])


class Brick:
    def __init__(self, start: Cube, end: Cube):
        self.start = start
        self.end = end

    @property
    def area(self):
        return [
            (i, j)
            for i in range(self.start.x, self.end.x + 1)
            for j in range(self.start.y, self.end.y + 1)
        ]

    def diff_z(self):
        return self.end.z - self.start.z

    def afterlife(self, peak):
        return Brick(
            Cube(self.start.x, self.start.y, peak),
            Cube(self.end.x, self.end.y, peak + self.diff_z()),
        )

    def can_fall(self, peak):
        return peak < self.start.z


def get_bricks(inp):
    bricks = []
    for line in inp:
        start, end = line.split("~")
        start = Cube(*map(int, start.split(",")))
        end = Cube(*map(int, end.split(",")))
        bricks.append(Brick(start, end))
    return sorted(bricks, key=lambda bricks: bricks.start.z)


def enumarate_skip(sequence, skip):
    for index, value in enumerate(sequence):
        if index == skip:
            continue
        yield index, value


def drop(bricks, skip=None):
    skyline = defaultdict(int)
    falls = 0
    for i, brick in enumarate_skip(bricks, skip):
        peak = max(skyline[a] for a in brick.area) + 1
        skyline.update({coord: peak + brick.diff_z() for coord in brick.area})
        bricks[i] = brick.afterlife(peak)
        falls += brick.can_fall(peak)
    return falls


bricks = get_bricks(inp)
drop(bricks)

total_a = 0
total_b = 0
for i in range(len(bricks)):
    falls = drop(bricks.copy(), i)
    total_a += not falls
    total_b += falls

puzzle.answer_a = total_a
puzzle.answer_b = total_b
