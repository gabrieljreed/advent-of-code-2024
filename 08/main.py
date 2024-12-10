from pathlib import Path


INPUT_PATH = Path(__file__).parent / "input.txt"

input = INPUT_PATH.read_text()

test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

INPUT = input


def get_all_signals_dict(input: str) -> dict[str, list[tuple[int, int]]]:
    all_signals = {}

    rows = input.splitlines()
    for i, row in enumerate(rows):
        for j, letter in enumerate(row):
            if letter == "\n" or letter == ".":
                continue
            if letter not in all_signals.keys():
                all_signals[letter] = []

            all_signals[letter].append((i, j))

    return all_signals


def add(p1, p2):
    return (p1[0] + p2[0]), (p1[1] + p2[1])


def sub(p1, p2):
    return (p1[0] - p2[0]), (p1[1] - p2[1])


def invert(x, y):
    return x * -1, y * -1


def get_antinodes(positions: list[tuple[int, int]], num_rows: int, num_cols: int) -> list[tuple[int, int]]:
    antinodes = set()
    for i, node_1 in enumerate(positions):
        for node_2 in positions[i + 1:]:
            distance = sub(node_1, node_2)
            antinode_1 = add(node_1, distance)
            if 0 <= antinode_1[0] < num_rows and 0 <= antinode_1[1] < num_cols:
                antinodes.add(antinode_1)

            inverse_distance = invert(*distance)
            antinode_2 = add(node_2, inverse_distance)
            if 0 <= antinode_2[0] < num_rows and 0 <= antinode_2[1] < num_cols:
                antinodes.add(antinode_2)

    return list(antinodes)


def get_antinodes_2(positions: list[tuple[int, int]], num_rows: int, num_cols: int) -> list[tuple[int, int]]:
    antinodes = set()
    for i, node_1 in enumerate(positions):
        for node_2 in positions[i + 1:]:
            distance = sub(node_1, node_2)
            antinode_1 = node_1
            while 0 <= antinode_1[0] < num_rows and 0 <= antinode_1[1] < num_cols:
                antinodes.add(antinode_1)
                antinode_1 = add(antinode_1, distance)

            inverse_distance = invert(*distance)
            antinode_2 = node_2
            while 0 <= antinode_2[0] < num_rows and 0 <= antinode_2[1] < num_cols:
                antinodes.add(antinode_2)
                antinode_2 = add(antinode_2, inverse_distance)

    return list(antinodes)


if __name__ == "__main__":
    all_signals = get_all_signals_dict(INPUT)

    rows = INPUT.splitlines()
    num_rows = len(rows)
    num_cols = len(rows[0])

    antinode_positions = set()
    for letter, positions in all_signals.items():
        # Part 1
        # antinodes = get_antinodes(positions, num_rows, num_cols)
        
        # Part 2
        antinodes = get_antinodes_2(positions, num_rows, num_cols)

        for antinode in antinodes:
            antinode_positions.add(antinode)

    print(len(antinode_positions))

