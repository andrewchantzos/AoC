class Grid:
    def __init__(self, inp):
        self.grid = inp
        self.length, self.height = self._inp_size()

    def _inp_size(self):
        length = len(self.grid[0])
        height = len(self.grid)
        return length, height

    def get_neighbors(self, line_num, pos, include_diagonal=True):
        neighbors = []

        for i in range(max(0, line_num - 1), min(self.length, line_num + 2)):
            for j in range(max(0, pos - 1), min(self.height, pos + 2)):
                if (i, j) != (line_num, pos) and (include_diagonal or i == line_num or j == pos):
                    neighbors.append((i, j))

        return neighbors

    def get_range_neighbours(self, line_num, start, end, include_diagonal=True):
        neighbours = set()
        for pos in range(start, end):
            neighbours.update(self.get_neighbors(line_num, pos, include_diagonal))
        return list(neighbours)

    def get(self, row, col):
        return self.grid[row][col]

    def __getitem__(self, pos):
        row, col = pos
        return self.grid[row][col]

    def get_column(self, pos):
        return [line[pos] for line in self.grid]

def read_file(day):
    with open(f"input/day{day}.txt") as f:
        return f.read().splitlines()
