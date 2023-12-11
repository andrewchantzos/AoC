import itertools


class Grid:
    def __init__(self, inp):
        self.grid = [list(line) for line in inp]

        self.length, self.height = self._inp_size()

    def _inp_size(self):
        length = len(self.grid[0])
        height = len(self.grid)
        return length, height

    def get_neighbors(self, row, col, include_diagonal=True):
        neighbors = []

        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.length, col + 2)):
                if (i, j) != (row, col) and (include_diagonal or i == row or j == col):
                    neighbors.append((i, j))

        return neighbors

    def get_range_neighbours(self, line_num, start, end, include_diagonal=True):
        neighbours = set()
        for pos in range(start, end):
            neighbours.update(self.get_neighbors(line_num, pos, include_diagonal))
        return list(neighbours)

    def get(self, row, col):
        return self.grid[row][col]

    def set(self, row, col, val):
        self.grid[row][col].replace(self.grid[row][col], val)

    def __getitem__(self, pos):
        row, col = pos
        return self.grid[row][col]

    def __setitem__(self, pos, val):
        row, col = pos
        self.grid[row][col] = val

    def get_column(self, pos):
        return [line[pos] for line in self.grid]

    def size(self):
        return self.length * self.height

    def inner_coordinates(self):
        return list(itertools.product(range(1, self.length - 1), range(1, self.height - 1)))

    def cross_coordinates(self, coord):
        row, col = coord
        left = [(row, i) for i in range(0, col)]
        right = [(row, i) for i in range(col + 1, self.length)]
        up = [(i, col) for i in range(0, row)]
        down = [(i, col) for i in range(row + 1, self.height)]

        return reversed(left), right, reversed(up), down

    def get_values(self, coords):
        return {coord: self[coord] for coord in coords}


def read_file(day):
    with open(f"input/day{day}.txt") as f:
        return f.read().splitlines()
