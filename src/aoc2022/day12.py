from aocd.models import Puzzle
from src.utils import *
import numpy as np
from itertools import count
import networkx as nx
from itertools import product

puzzle = Puzzle(year=2022, day=12)

inp = puzzle.example_data

inp = puzzle.input_data.splitlines()

G = nx.DiGraph()

grid = Grid(inp)

start = None
end = None
a_coordinates = []
for coord in product(range(grid.height), range(grid.length)):
    if grid[coord] == "S":
        start = coord
        grid[start] = "a"
    if grid[coord] == "E":
        end = coord
        grid[end] = "z"
    if grid[coord] == "a":
        a_coordinates.append(coord)
    for neighbour in grid.get_neighbors(coord[0], coord[1], include_diagonal=False):
        if ord(grid[coord]) + 1 >= ord(grid[neighbour]):
            G.add_edge(coord, neighbour)


puzzle.answer_a = nx.shortest_path_length(G, start, end)

paths = []
for x in a_coordinates:
    try:
        paths.append(nx.shortest_path_length(G, x, end))
    except Exception:
        pass

puzzle.answer_b = min(paths)
