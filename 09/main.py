from pathlib import Path
from itertools import batched

input_file = Path(__file__).parent / "input.txt"
input = input_file.read_text().strip()

test_input_1 = "2333133121414131402"
test_input_2 = "12345"
test_input_3 = input[:21]


INPUT = test_input_1


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


def compress_files(input: list[str]) -> list[str]:
    result = input.copy()
    free_space_start = 0
    free_space_end = 0
    file_start = len(result) - 1
    file_end = len(result) - 1

    while result[free_space_start] != ".":
        free_space_start += 1
    free_space_end = free_space_start
    while result[free_space_end] == ".":
        free_space_end += 1

    while result[file_start] == ".":
        file_start -= 1
    current_file = result[file_start]
    file_end = file_start
    while result[file_end] == current_file:
        file_end -= 1

    len_free_space = free_space_end - free_space_start

    len_file = file_start - file_end

    pointers = [" " for _ in result]
    pointers[free_space_start] = "v"
    pointers[free_space_end] = "v"
    pointers[file_start] = "V"
    pointers[file_end] = "V"
    print(pointers)
    tmp_for_print = [str(i) for i in result]
    print(tmp_for_print)
    print(len_free_space)
    print(len_file)

    """Pseudo code for this:
    for file in files:
        len_file = get_len_file(file)
        next_free_space = get_next_free_space(0)
        len_free_space = get_len_free_space(first_free_space)
        while len_file > len_free_space:
            next_free_space = get_next_free_space(next_free_space)
            if out_of_bounds:
                continue to next file
            len_free_space = get_len_free_space(next)
        move file to free space
    """

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


def part_2():
    disk_map = parse_memory_block(INPUT)
    compressed = compress_files(disk_map)
    # print(compute_checksum(compressed))


if __name__ == "__main__":
    part_2()
