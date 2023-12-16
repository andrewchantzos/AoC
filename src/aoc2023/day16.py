from aocd.models import Puzzle
from src.utils import *

puzzle = Puzzle(year=2023, day=16)


inp = puzzle.input_data.splitlines()

grid = Grid(inp)


def get_next(g, coord, dir):
    def directions():
        match (g[coord], dir):
            case (".", _):
                return [dir]
            case ("|", Direction.L) | ("|", Direction.R):
                return [Direction.U, Direction.D]
            case ("-", Direction.U) | ("-", Direction.D):
                return [Direction.L, Direction.R]
            case ("-" | "|", _):
                return [dir]
            case ("\\", Direction.U):
                return [Direction.L]
            case ("\\", Direction.D):
                return [Direction.R]
            case ("\\", Direction.R):
                return [Direction.D]
            case ("\\", Direction.L):
                return [Direction.U]
            case ("/", Direction.U):
                return [Direction.R]
            case ("/", Direction.D):
                return [Direction.L]
            case ("/", Direction.R):
                return [Direction.U]
            case ("/", Direction.L):
                return [Direction.D]
            case (_, _):
                return []

    return [(g.move_dir(coord, dir), dir) for dir in directions()]


def dfs(start, direction, visited=None):
    if visited is None:
        visited = set()
    visited.add((start, direction))

    for neighbor, direction in get_next(grid, start, direction):
        if neighbor and (neighbor, direction) not in visited:
            dfs(neighbor, direction, visited)
    return visited


# Slightly faster
def dfs_iterative(start, direction):
    stack = [(start, direction)]
    visited = set()

    while stack:
        current, current_direction = stack.pop()
        visited.add((current, current_direction))

        for neighbor, next_direction in get_next(grid, current, current_direction):
            if neighbor and (neighbor, next_direction) not in visited:
                stack.append((neighbor, next_direction))
    return visited


initials = []
for i in range(grid.length):
    initials.append(((0, i), Direction.D))
    initials.append(((grid.height - 1, i), Direction.U))
for i in range(grid.height):
    initials.append(((i, 0), Direction.R))
    initials.append(((i, grid.length - 1), Direction.L))


def v_len(visited):
    return len(set(x[0] for x in visited))


puzzle.answer_a = v_len(dfs_iterative((0, 0), Direction.R))
puzzle.answer_b = max(v_len(dfs_iterative(s, d)) for s, d in initials)
