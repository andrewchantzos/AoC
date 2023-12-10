from tokenize import blank_re
from aocd.models import Puzzle
from src.utils import *
import numpy as np
from itertools import product
import networkx as nx

puzzle = Puzzle(year=2023, day=10)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()

grid = Grid(inp)
G = nx.DiGraph()

start = None

directions = {
    "*": [(1, 0), (0, 1)],
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "J": [(-1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "7": [(1, 0), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "S": [(-1, 0), (0, -1)],
    ".": [],
}

allowed = {"U": ["|", "7", "F"], "D": ["|", "L", "J"], "L": ["-", "7", "J"], "R": ["-", "L", "F"]}

for coord in product(range(grid.height), range(grid.length)):
    val = grid[coord]
    if grid[coord] == "S":
        start = coord
        (row, col) = coord
        if grid[(row - 1, col)] in allowed["U"]:
            G.add_edge(start, (row - 1, col))
        if grid[(row + 1, col)] in allowed["D"]:
            G.add_edge(start, (row + 1, col))
        if grid[(row, col - 1)] in allowed["R"]:
            G.add_edge(start, (row, col - 1))
        if grid[(row, col + 1)] in allowed["L"]:
            G.add_edge(start, (row, col + 1))
        continue
    for di, dj in directions[val]:
        G.add_edge(coord, (coord[0] + di, coord[1] + dj))


# Manually find end by calculating the paths
def get_end():
    row, col = start
    potential_ends = [
        ((row - 1, col), "U"),
        ((row + 1, col), "D"),
        ((row, col + 1), "R"),
        ((row, col - 1), "L"),
    ]
    for coord, move in potential_ends:
        to_add = False
        if G.has_edge(start, coord):
            G.remove_edge(start, coord)
            to_add = True
        l = nx.shortest_path_length(G, start, coord)

        if l > 0 and grid[coord] in allowed[move]:
            # Found the end, don't add edge back
            return coord
        if to_add:
            # Add it only if it's not the end
            G.add_edge(start, coord)


puzzle.answer_a = int((nx.shortest_path_length(G, start, get_end()) + 1) / 2)


# Get the loop path
loop = nx.shortest_path(G, start, get_end())


# Make a double-sized graph to allow floodfill
# This is useful for the squeezing pipes
all_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
DG = nx.Graph()
for i, j in product(range(-2, 2 * len(inp) + 2), range(-2, 2 * len(inp[0]) + 2)):
    for di, dj in all_directions:
        DG.add_edge((i, j), (i + di, j + dj))


extended_loop_nodes = set()
for i, j in loop:
    extended_loop_nodes.add((2 * i, 2 * j))
    for di, dj in directions[grid[(i, j)]]:
        extended_loop_nodes.add((2 * i + di, 2 * j + dj))

# Remove all nodes of the loop
for node in extended_loop_nodes:
    DG.remove_node(node)

# Find connected components
total_isolated = set()
for x in nx.connected_components(DG):
    # If the connected component flooded the grid
    # it will reach the end
    if (-2, -2) not in x:
        total_isolated.update(x)

# Count only the ones in the original graph (even ones)
puzzle.answer_b = sum([1 for i, j in total_isolated if i % 2 == j % 2 == 0])
