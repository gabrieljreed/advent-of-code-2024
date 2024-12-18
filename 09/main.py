from pathlib import Path
from itertools import batched

input_file = Path(__file__).parent / "input.txt"
input = input_file.read_text().strip()

test_input_1 = "2333133121414131402"
test_input_2 = "12345"
test_input_3 = input[:21]


INPUT = input


def parse_memory_block(input: str) -> list[str]:
    input = input.strip()
    result = []
    is_file = True
    file_counter = 0
    for char in input:
        if is_file:
            result.extend([file_counter for _ in range(int(char))])
            file_counter += 1
        else:
            result.extend([c for c in "." * int(char)])

        is_file = not is_file

    return result


def compress_block(input: list[str]) -> list[str]:
    result = input.copy()
    front = 0
    end = len(result) - 1

    while True:
        while result[front] != ".":
            front += 1

        while result[end] == ".":
            end -= 1

        if front >= end:
            break

        result[front], result[end] = result[end], result[front]

    return result


def compute_checksum(input: list[str]) -> int:
    total = 0

    for i, letter in enumerate(input):
        if letter == ".":
            continue
        total += i * int(letter)

    return total


def part_1():
    disk_map = parse_memory_block(INPUT)
    compressed = compress_block(disk_map)
    print(compute_checksum(compressed))


if __name__ == "__main__":
    part_1()
