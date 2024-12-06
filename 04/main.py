from pathlib import Path
from enum import Enum, auto
from typing import Optional

INPUT_FILE = Path(__file__).parent / "input.txt"
with open(INPUT_FILE, "r") as f:
    input = f.read()

TARGET_WORD_1 = "XMAS"
TARGET_WORD_2 = "MAS"

test_input = """....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
"""

test_input_2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""

class Direction(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)

class Text:
    def __init__(self, text: str):
        self.text = text
        self.rows = text.splitlines()
        self._cur_row = 0
        self._cur_col = 0

    def __iter__(self):
        self._cur_row = 0
        self._cur_col = 0
        return self

    def __next__(self):
        self._cur_col += 1
        if self._cur_col >= self.num_cols:
            self._cur_col = 0
            self._cur_row += 1
        if self._cur_row >= self.num_rows:
            raise StopIteration

        return self._cur_row, self._cur_col

    def get(self, row: int, col: int) -> str:
        if not self.check_bounds(row, col):
            raise IndexError(f"({row}, {col}) is out of range 0-{self.num_rows - 1}")
        current_row = self.rows[row]
        return current_row[col]

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_cols(self) -> int:
        if not self.num_rows:
            return 0
        return len(self.rows[0])

    def check_bounds(self, row: int, col: int) -> bool:
        if row < 0 or col < 0:
            return False
        if row >= self.num_rows or col >= self.num_cols:
            return False
        return True

    def get_sequence_coords(self, row: int, col: int, direction: Direction) -> Optional[list[tuple[int, int]]]:
        """Get a sequence starting from a given row and col in a given direction."""
        result = [(row, col)]
        for i in range(len(TARGET_WORD_1) - 1):
            row = row + direction.value[0]
            col = col + direction.value[1]
            if not self.check_bounds(row, col):
                return None
            result.append((row, col))

        return result

    def get_sequence(self, sequence: list[tuple[int, int]]) -> str:
        """Get a sequence of letters given a sequence of points."""
        result = ""
        for point in sequence:
            row, col = point
            result += self.get(row, col)
        return result

    def check_sequence(self, sequence: list[tuple[int, int]]) -> bool:
        """Check if the given sequence of letters contains the target word."""
        for i, point in enumerate(sequence):
            row, col = point
            if self.get(row, col) != TARGET_WORD_1[i]:
                return False
        return True

    def get_x_coords(self, row, col) -> Optional[list[tuple[int, int]]]:
        """Get the coordinates that form an 'X' of the given point, if a valid one can be made."""
        result = []
        directions = [Direction.NW.value, (0, 0), Direction.SE.value, Direction.SW.value, (0, 0), Direction.NE.value]
        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]
            if not self.check_bounds(new_row, new_col):
                return None
            result.append((new_row, new_col,))

        return result

    def print_x_coords(self, coords: list[tuple[int, int]]):
        result = f"{self.get(*coords[0])}.{self.get(*coords[5])}\n"
        result += f".{self.get(*coords[1])}.\n"
        result += f"{self.get(*coords[3])}.{self.get(*coords[2])}\n"
        print(result)

    def check_x_coords(self, coords: list[tuple[int, int]]) -> bool:
        cross_1 = "".join([self.get(*coord) for coord in coords[:3]])
        cross_2 = "".join([self.get(*coord) for coord in coords[3:]])
        return (cross_1 == "MAS" or cross_1 == "SAM") and (cross_2 == "MAS" or cross_2 == "SAM")


def part_1():
    total = 0
    text = Text(input)

    for point in text:
        row, col = point
        for direction in Direction:
            coords = text.get_sequence_coords(row, col, direction)
            if not coords:
                continue
            if text.check_sequence(coords):
                total += 1

    return total


def part_2():
    total = 0
    text = Text(input)

    for point in text:
        row, col = point
        coords = text.get_x_coords(row, col)
        if not coords:
            continue
        if text.check_x_coords(coords):
            total += 1

    return total


if __name__ == "__main__":
    print(part_1())
    print(part_2())

