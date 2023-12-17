from aocd.models import Puzzle
from src.utils import *
from collections import namedtuple
import heapq
import nographs as nog

puzzle = Puzzle(year=2023, day=17)


State = namedtuple("State", ["coord", "direction", "moves", "weight"])


def neighbours(grid, state, min_moves=1, max_moves=4):
    result = []

    for dir in Direction:
        new_coord = dir.move(state.coord)
        moves = state.moves + 1 if dir == state.direction else 1
        if not grid.is_in(new_coord):
            continue
        if moves > max_moves:
            continue
        if dir.opposite() == state.direction:
            continue
        if dir != state.direction and state.moves < min_moves:
            continue
        result.append(State(coord=new_coord, direction=dir, moves=moves, weight=grid[new_coord]))
    return result


def dijkstra(grid, start, end, min_moves=1, max_moves=3):
    frontier = [
        (0, State(coord=start, direction=dir, moves=0, weight=grid[start])) for dir in Direction
    ]
    distances = {}

    while frontier:
        current_distance, current_node = heapq.heappop(frontier)

        if current_node in distances:
            continue

        distances[current_node] = current_distance

        if current_node.coord == end and current_node.moves > min_moves:
            return distances[current_node]

        for neighbour in neighbours(grid, current_node, min_moves, max_moves):
            if neighbour not in distances:
                new_distance = distances[current_node] + neighbour.weight
                heapq.heappush(frontier, (new_distance, neighbour))

    return -1


def get_min_nog(grid, start, end, min_moves=1, max_moves=3):
    def next_edges(state, _):
        for x in neighbours(grid, state, min_moves, max_moves):
            yield x, x.weight

    t = nog.TraversalShortestPaths(next_edges)
    start_vertices = [
        State(coord=start, direction=dir, moves=0, weight=grid[start]) for dir in Direction
    ]
    for node in t.start_from(start_vertices=start_vertices):
        if node.coord == end and node.moves > min_moves:
            return t.distance
          
grid = Grid(puzzle.input_data.splitlines(), mapper=lambda x: list(int(s) for s in x))


start = (0, 0)
end = grid.end
puzzle.answer_a = dijkstra(grid, start, end)
puzzle.answer_b = dijkstra(grid, start, end, min_moves=4, max_moves=10)
