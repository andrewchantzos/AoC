from typing import Tuple, List, Callable, Any, Iterable, TypeVar
import itertools

Coordinates = Tuple[int, int]
T = TypeVar("T", int, str, float, complex)


class Grid:
    """
    A class representing a 2D grid.
    """

    def __init__(self, inp: list[str], mapper: Callable[[str], List[T]] = list):
        """
        A class representing a 2D grid.

        Parameters:
        - inp (List[str]): A list of strings representing the grid.
        - mapper (Callable[[str], List[T]]): A function to map each line in inp. Default is list().

        Attributes:
        - grid (list): A 2D list representing the grid.
        - length (int): The length (number of columns) of the grid.
        - height (int): The height (number of rows) of the grid.
        """
        self.grid = [mapper(line) for line in inp]
        self.length, self.height = len(self.grid[0]), len(self.grid)

    def get_neighbors(self, row: int, col: int, include_diagonal=True) -> List[Coordinates]:
        """
        Get the neighboring coordinates of a given position.

        Parameters:
        - `row` (int): The row index of the position.
        - `col` (int): The column index of the position.
        - `include_diagonal` (bool): Whether to include diagonal neighbors.

        Returns:
        `list[Coordinates]`: A list of neighboring coordinates.
        """
        neighbors = []

        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.length, col + 2)):
                if (i, j) != (row, col) and (include_diagonal or i == row or j == col):
                    neighbors.append((i, j))

        return neighbors

    def get_range_neighbors(
        self, line_num: int, start: int, end: int, include_diagonal=True
    ) -> list[Coordinates]:
        """
        Get the neighboring coordinates within a range of positions in a specific line.

        Parameters:
        - `line_num` (int): The index of the line.
        - `start` (int): The starting position in the line.
        - `end` (int): The ending position in the line.
        - `include_diagonal` (bool): Whether to include diagonal neighbors.

        Returns:
        `list[Coordinates]`: A list of neighboring coordinates.
        """
        return list(
            set(
                itertools.chain.from_iterable(
                    self.get_neighbors(line_num, pos, include_diagonal) for pos in range(start, end)
                )
            )
        )

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

    def get_row(self, pos):
        return self.grid[pos]

    def columns(self):
        for i in range(self.length):
            yield [line[i] for line in self.grid]

    def set_column(self, column, pos):
        for i in range(self.length):
            self[(i, pos)] = column[i]

    def get_column(self, pos):
        return [line[pos] for line in self.grid]

    def rows(self):
        for line in self.grid:
            yield line

    def set_row(self, row, pos):
        self.grid[pos] = row

    def items(self) -> Iterable[Tuple[Coordinates, T]]:
        """
        Get an iterable of tuples representing the coordinates and values of each element in the grid.

        Returns:
        Iterable[Tuple[Coordinates, T]]: An iterable of tuples where each tuple contains a coordinate
        and the corresponding value in the grid.
        """
        for coord in itertools.product(range(self.height), range(self.length)):
            yield coord, self[coord]

    def size(self) -> int:
        """
        Get the size of the grid

        Returns:
        int: Size of grid
        """
        return self.length * self.height

    def inner_coordinates(self) -> list[Coordinates]:
        """
        Get the coordinates of inner points in the grid, excluding the boundary.

        Returns:
        List[Coordinates]: A list of coordinate tuples representing inner points in the grid.
        """
        return list(itertools.product(range(1, self.length - 1), range(1, self.height - 1)))

    def flip(self, coord1, coord2):
        self[coord1], self[coord2] = self[coord2], self[coord1]

    def cross_coordinates(
        self, coord: Coordinates
    ) -> Tuple[
        Iterable[Coordinates], Iterable[Coordinates], Iterable[Coordinates], Iterable[Coordinates]
    ]:
        """
        Get the coordinates forming a cross pattern around a specified coordinate.
        Parameters:
        - coord (Coordinates): The coordinate (row, column) around which the cross pattern is formed.

        Returns:
        A tuple containing four iterables representing the coordinates of the left, right, up, and down arms
        of the cross pattern, respectively.
        """
        row, col = coord
        left = [(row, i) for i in range(0, col)]
        right = [(row, i) for i in range(col + 1, self.length)]
        up = [(i, col) for i in range(0, row)]
        down = [(i, col) for i in range(row + 1, self.height)]

        return reversed(left), right, reversed(up), down

    def get_values(self, coords: Iterable[Coordinates]) -> dict[Coordinates, T]:
        return {coord: self[coord] for coord in coords}

    def get_coords_for_value(self, value: T) -> list[Coordinates]:
        return [coord for coord, c in self.items() if c == value]

    def display(self):
        for line in self.grid:
            print(line)
        print()


def read_file(day):
    with open(f"input/day{day}.txt") as f:
        return f.read().splitlines()
