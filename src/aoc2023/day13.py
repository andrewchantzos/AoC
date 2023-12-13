from aocd.models import Puzzle
from src.utils import *

puzzle = Puzzle(year=2023, day=13)


grid_lines = puzzle.input_data.split(2 * "\n")


def reflections(grid):
    def get_lines(limit, fun):
        lines = []
        for i in range(1, limit):
            lim = min(limit - i, i)
            part1 = [fun(j) for j in reversed(range(i - lim, i))]
            part2 = [fun(j) for j in range(i, i + lim)]
            if part1 == part2:
                lines.append(i)
        return lines

    vertical = get_lines(grid.length, grid.get_column)
    horizontal = get_lines(grid.height, grid.get_row)

    return vertical, horizontal


def generate(grid):
    for coord, el in grid.items():
        grid[coord] = "#" if el == "." else "."
        yield grid
        # reset
        grid[coord] = el


def smudge(grid):
    init_vertical, init_horizontal = reflections(grid)
    for altered_grid in generate(grid):
        vertical, horizontal = reflections(altered_grid)
        # Remove matching elements
        if init_vertical and init_vertical[0] in vertical:
            vertical.remove(init_vertical[0])
        if init_horizontal and init_horizontal[0] in horizontal:
            horizontal.remove(init_horizontal[0])

        if len(vertical + horizontal) == 1:
            return vertical, horizontal
    return [], []


def get_value(vertical, horizontal):
    return vertical[0] if vertical else horizontal[0] * 100


grids = [Grid(x.splitlines()) for x in grid_lines]


puzzle.answer_a = sum(get_value(*reflections(grid)) for grid in grids)


puzzle.answer_b = sum(get_value(*smudge(grid)) for grid in grids)
