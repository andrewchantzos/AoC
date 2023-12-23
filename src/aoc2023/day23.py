from aocd.models import Puzzle
from src.utils import *
import networkx as nx

DIR_LOOKUP = {">": Direction.R, "<": Direction.L, "v": Direction.D}


puzzle = Puzzle(year=2023, day=23)


def get_max_path(g, source, target):
    return max(
        nx.path_weight(g, p, weight="weight") for p in nx.all_simple_paths(g, source, target)
    )


def p1_graph(grid):
    # A directed graph is needed for p1
    G = nx.grid_2d_graph(grid.height, grid.length, create_using=nx.DiGraph)
    nx.set_edge_attributes(G, 1, "weight")

    for coord, value in grid.items():
        if value == "#":
            G.remove_node(coord)
        if value in DIR_LOOKUP:
            # remove opposite edges
            op = DIR_LOOKUP[value].opposite().move(coord)
            G.remove_edge(coord, op)
    return G


def p2_graph(grid):
    G = nx.grid_2d_graph(grid.height, grid.length)
    nx.set_edge_attributes(G, 1, "weight")

    for coord, value in grid.items():
        if value == "#":
            G.remove_node(coord)

    def prune(g, source, target):
        for node in list(g.nodes):
            if node in (source, target) or node not in g:
                continue
            neighbors = list(g.neighbors(node))
            if len(neighbors) == 2:
                g.add_edge(
                    *neighbors, weight=sum(g.get_edge_data(x, node)["weight"] for x in neighbors)
                )
            if len(neighbors) <= 2:
                g.remove_node(node)

    prune(G, source, target)
    return G


grid = Grid(puzzle.input_data.splitlines())

source = (0, 1)
target = (grid.height - 1, grid.length - 2)

# Second part runs in around 2 minutes
puzzle.answer_a = get_max_path(p1_graph(grid), source, target)
puzzle.answer_b = get_max_path(p2_graph(grid), source, target)
