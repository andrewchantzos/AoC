from aocd.models import Puzzle
from src.utils import *
from itertools import product
from itertools import combinations

puzzle = Puzzle(year=2023, day=11)


inp = puzzle.input_data.splitlines()


grid = Grid(inp)
galaxies = [x for x in product(range(grid.height), range(grid.length)) if grid[x] == "#"]

extra_rows = [x for x, line in enumerate(inp) if all(char == "." for char in line)]

extra_columns = [i for i in range(len(inp[0])) if all(row[i] == "." for row in inp)]


def new_galaxies(galaxies, multi):
    new_galaxies = []
    for x in galaxies:
        rows = len([r for r in extra_rows if r < x[0]])
        cols = len([c for c in extra_columns if c < x[1]])
        new_galaxies.append((x[0] + rows * multi, x[1] + cols * multi))
    return new_galaxies


def diff(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


puzzle.answer_a = sum(diff(a, b) for a, b in combinations(new_galaxies(galaxies, 1), 2))

puzzle.answer_b = sum(diff(a, b) for a, b in combinations(new_galaxies(galaxies, (1000000 - 1)), 2))
