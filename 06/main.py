from pathlib import Path
from enum import Enum
from dataclasses import dataclass

INPUT_FILE = Path(__file__).parent / "input.txt"
with open(INPUT_FILE, "r") as f:
    input = f.read()


OBSTACLE_CHARACTER = "#"
TEMP_OBSTACLE_CHARACTER = "O"
PATH_CHARACTER = "X"

test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def turn(self):
        next_value = (self.value + 1) % len(Direction)
        return Direction(next_value)

    def get_movement(self):
        if self.name == "N":
            return (-1, 0)
        elif self.name == "E":
            return (0, 1)
        elif self.name == "S":
            return (1, 0)
        else:
            return (0, -1)

    def get_character(self):
        if self.name == "N":
            return "^"
        elif self.name == "E":
            return ">"
        elif self.name == "S":
            return "v"
        else:
            return "<"

    # N = (-1, 0)
    # E = (0, 1)
    # S = (1, 0)
    # W = (0, -1)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if hasattr(other, "__getitem__"):
            return Point(self.x + other[0], self.y + other[1])
        else:
            return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Guard:
    def __init__(self, map: str):
        self.map = map
        self.rows = map.splitlines()
        self.position = Point(-1, -1)
        self._get_starting_position()
        self.current_direction = Direction.N
        self.num_unique_positions_visited = 1
        self.visited = set()
        self.visited.add((self.position, self.current_direction))

    def __iter__(self):
        self._current_point = Point(0, 0)
        return self

    def __next__(self):
        self._current_point.y += 1
        if self._current_point.y >= self.num_cols:
            self._current_point.y = 0
            self._current_point.x += 1
        if self._current_point.x >= self.num_rows:
            raise StopIteration

        return self._current_point

    def __str__(self):
        return "\n".join(self.rows)

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_cols(self) -> int:
        if not self.num_rows:
            return 0
        return len(self.rows[0])

    def _check_bounds(self, point: Point) -> bool:
        if point.x < 0 or point.y < 0:
            return False
        if point.x >= self.num_rows or point.y >= self.num_cols:
            return False
        return True

    def _get_starting_position(self):
        for row in self.rows:
            if "^" in row:
                row_index = self.rows.index(row)
                col_index = row.index("^")
                self.position = Point(row_index, col_index)

    def get(self, point: Point) -> str:
        current_row = self.rows[point.x]
        return current_row[point.y]

    def set(self, point: Point, value: str):
        current_row = self.rows[point.x]
        new_row = current_row[:point.y] + value + current_row[point.y + 1:]
        self.rows[point.x] = new_row

    def is_blocked(self, point: Point) -> bool:
        return self.get(point) == OBSTACLE_CHARACTER or self.get(point) == TEMP_OBSTACLE_CHARACTER

    def walk(self) -> bool:
        """Simulate the guard walking around, returns true if the guard successfully exits, false if it loops."""
        next_position = self.position + self.current_direction.get_movement()

        while self._check_bounds(next_position):
            # Turn if we're going to hit an obstacle
            if self.is_blocked(next_position):
                self.current_direction = self.current_direction.turn()
                next_position = self.position + self.current_direction.get_movement()

            self.set(self.position, PATH_CHARACTER)
            if self.get(next_position) != PATH_CHARACTER:
                self.num_unique_positions_visited += 1
            self.set(next_position, self.current_direction.get_character())

            if (next_position, self.current_direction) in self.visited:
                return False
            self.visited.add((next_position, self.current_direction))

            self.position = next_position
            next_position = self.position + self.current_direction.get_movement()

        return True


def part_1():
    guard = Guard(input)
    guard.walk()
    print(guard.num_unique_positions_visited)


def part_2():
    guard = Guard(input)
    total = 0

    for point in guard:
        if guard.get(point) == OBSTACLE_CHARACTER or guard.get(point) == "^":
            continue

        test_guard = Guard(input)
        print(f"Testing point {point}")
        test_guard.set(point, TEMP_OBSTACLE_CHARACTER)

        if not test_guard.walk():
            total += 1

    print(total)

if __name__ == "__main__":
    # part_1()
    part_2()

