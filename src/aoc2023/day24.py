import numpy as np
from aocd.models import Puzzle
import itertools
from sympy import Symbol, solve_poly_system

puzzle = Puzzle(year=2023, day=24)

lines = puzzle.input_data.splitlines()

lower = 200000000000000
upper = 400000000000000


def is_intersection(x1, y1, dx1, dy1, x2, y2, dx2, dy2):
    slope1, slope2 = dy1 / dx1, dy2 / dx2
    if slope1 == slope2:
        return False
    # Solve the system of equations Ax = B
    A = np.array([[slope1, -1], [slope2, -1]])
    b = np.array([slope1 * x1 - y1, slope2 * x2 - y2])
    x, y = np.linalg.solve(A, b)
    if not (lower <= x <= upper and lower <= y <= upper):
        return False
    # Get times, they have to be positive
    t1 = (x - x1) / dx1
    t2 = (x - x2) / dx2
    return t1 > 0 and t2 > 0


hailstones = []
for line in lines:
    pos_str, vel_str = map(str.strip, line.split("@"))
    x, y, z = map(int, pos_str.split(","))
    dx, dy, dz = map(int, vel_str.split(","))
    hailstones.append((x, y, z, dx, dy, dz))

# part 1
total = 0
for a, b in itertools.combinations(hailstones, 2):
    x1, y1, _, dx1, dy1, _ = a
    x2, y2, _, dx2, dy2, _ = b

    total += is_intersection(x1, y1, dx1, dy1, x2, y2, dx2, dy2)

puzzle.answer_a = int(total)

# part 2

equations = []
t_symbols = []
throw_x = Symbol("x")
throw_y = Symbol("y")
throw_z = Symbol("z")
throw_dx = Symbol("dx")
throw_dy = Symbol("dy")
throw_dz = Symbol("dz")

# part 2
# Only need to solve a 9x9 system to determine all the variables
# x, y, z, dx, dy, dz, t1, t2, t3
# The throw crosses each line at different times
# throw_pos + throw_velocity * t = stone_pos + stone_velocity * t
for i, shard in enumerate(hailstones[:3]):
    x1, y1, z1, dx, dy, dz = shard
    t = Symbol("t" + str(i))

    equation_x = throw_x + throw_dx * t - x1 - dx * t
    equation_y = throw_y + throw_dy * t - y1 - dy * t
    equation_z = throw_z + throw_dz * t - z1 - dz * t

    equations.extend([equation_x, equation_y, equation_z])
    t_symbols.append(t)

result = solve_poly_system(
    equations, *([throw_x, throw_y, throw_z, throw_dx, throw_dy, throw_dz] + t_symbols)
)
x, y, z, *_ = result[0]
puzzle.answer_b = int(x + y + z)
