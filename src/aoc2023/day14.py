from aocd.models import Puzzle
from src.utils import *
import itertools

puzzle = Puzzle(year=2023, day=14)


inp = puzzle.input_data.splitlines()

# inp = """O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....""".splitlines()

grid = Grid(inp)


def move_Os_left(lst):
    for i, el in enumerate(lst):
        if el != "O":
            continue
        for j in range(i - 1, -1, -1):
            if lst[j] == "#":
                break
            lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def move_direction(grid, direction):
    if direction == "N":
        for i, column in enumerate(grid.columns()):
            column = move_Os_left(column)
            grid.set_column(column, i)
    if direction == "S":
        for i, column in enumerate(grid.columns()):
            column.reverse()
            column = move_Os_left(column)
            column.reverse()
            grid.set_column(column, i)
    if direction == "W":
        for i, row in enumerate(grid.rows()):
            row = move_Os_left(row)
            grid.set_row(row, i)
    if direction == "E":
        for i, row in enumerate(grid.rows()):
            row.reverse()
            row = move_Os_left(row)
            row.reverse()
            grid.set_row(row, i)


def calculate_total(grid):
    total = 0
    for i, row in enumerate(reversed(list(grid.rows())), start=1):
        total += row.count("O") * i
    return total


move_direction(grid, "N")

puzzle.answer_a = calculate_total(grid)


def part_two(grid):
    cycles = {}
    for i in itertools.count(start=1):
        move_direction(grid, "N")
        move_direction(grid, "W")
        move_direction(grid, "S")
        move_direction(grid, "E")
        s = frozenset(grid.get_coords_for_value("O"))

        if s in cycles:
            repeat = i - cycles[s]
            if (1_000_000_000 - i) % repeat == 0:
                return calculate_total(grid)
        cycles[s] = i


puzzle.answer_b = part_two(grid)
