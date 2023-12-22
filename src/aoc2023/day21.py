from aocd.models import Puzzle
from src.utils import *
import nographs as nog
from collections import deque, defaultdict
import numpy as np

puzzle = Puzzle(year=2023, day=21)

inp = puzzle.input_data.splitlines()


grid = Grid(inp)


def bfs_with_depth(grid, start, target_depth):
    queue = deque([(start, 0)])
    steps = defaultdict(set)
    visited = set()
    while queue:
        current_node, depth = queue.popleft()
        neighbours = [
            d.move(current_node) for d in Direction if grid.get(d.move(current_node)) != "#"
        ]

        if depth < target_depth and current_node not in visited:
            # Enqueue neighbors with increased depth
            queue.extend((neighbor, depth + 1) for neighbor in neighbours)
            steps[depth].update(neighbours)
            visited.add(current_node)
    return steps


def bfs_steps(x):
    start = grid.get_coords_for_value("S")[0]
    steps = bfs_with_depth(grid, start, x)
    # The way we calculate the steps, we need to add the nodes of
    # all the even or odd steps to get the correct result
    s = set.union(*(steps[i] for i in range((x + 1) % 2, x, 2)))
    return len(s)


puzzle.answer_a = bfs_steps(64)


def evaluate_quadratic_equation(points, x):
    # Fit a quadratic polynomial (degree=2) through the points
    coefficients = np.polyfit(*zip(*points), 2)

    # Evaluate the quadratic equation at the given x value
    result = np.polyval(coefficients, x)

    return round(result)


# For part two, the input is a square with length 131
# and the starting point is in the middle at length (65, 65)
# Probing the input we notice that 26501365 = 202300 * 131 + 65
# Making the assumption that this follows a polynomial equation
# we quickly realise it is a quadratic equation.
# 3 points to extrapolate for x=202300
f = lambda x: bfs_steps(65 + x * 131)
points = [(x, f(x)) for x in range(3)]
puzzle.answer_b = evaluate_quadratic_equation(points, 202300)


# Another solution based on nographs library


def multiply_inp(inp, times):
    new_grid = []
    for line in inp:
        new_grid.append(line * times)
    return new_grid * times


def nog_get_depth(maze, start, depth):
    next_vertices = maze.next_vertices_from_forbidden("#", wrap=True)

    traversal = nog.TraversalBreadthFirst(next_vertices)

    trip = traversal.start_from(start)

    s = set()
    # Manually handle start
    if depth % 2 == 0:
        s.add(start)
    for i in range(depth % 2, depth + 1, 2):
        nodes = trip.go_for_depth_range(i, i + 1)
        s.update(set(nodes))

    return len(s)


# I am lazy, so just multiply the matrix by 16
maze = nog.Array(multiply_inp(inp, 16), 2)
start = nog.Position(maze.findall("S")[0])

puzzle.answer_a = nog_get_depth(maze, start, 64)
points = [(x, nog_get_depth(maze, start, 65 + x * 131)) for x in range(3)]
puzzle.answer_b = evaluate_quadratic_equation(points, 202300)
