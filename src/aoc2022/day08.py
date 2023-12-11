from aocd.models import Puzzle
from src.utils import *

puzzle = Puzzle(year=2022, day=8)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()


grid = Grid(inp)

border_coordinates_size = grid.size() - len(grid.inner_coordinates())

visible_coords = set()
for coord in grid.inner_coordinates():
    res = grid.cross_coordinates(coord)
    curr_val = grid[coord]
    for combo in res:
        values = grid.get_values(combo).values()
        if all(curr_val > value for value in values):
            visible_coords.add(coord)


puzzle.answer_a = border_coordinates_size + len(visible_coords)


scenic_scores = []
for coord in grid.inner_coordinates():
    res = grid.cross_coordinates(coord)
    curr_val = grid[coord]
    scenic_score = 1
    for combo in res:
        curr_look = 0
        for item in combo:
            curr_look += 1
            if grid[item] >= curr_val:
                break
        if curr_look:
            scenic_score = scenic_score * curr_look
    scenic_scores.append(scenic_score)

puzzle.answer_b = max(scenic_scores)
