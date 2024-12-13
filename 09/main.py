from pathlib import Path

input_file = Path(__file__).parent / "input.txt"
input = input_file.read_text()

test_input_1 = "2333133121414131402"
test_input_2 = "12345"


INPUT = test_input_1


def parse_memory_block(input: str) -> str:
    input = input.strip()
    result = ""
    is_file = True
    file_counter = 0
    for letter in input:
        if is_file:
            result += str(file_counter) * int(letter)
            file_counter += 1
        else:
            result += "." * int(letter)

        is_file = not is_file

    return result


def compress_block(input: str) -> str:
    result = [letter for letter in input]
    # print(result)

    while "." in result:
        if result[-1] == ".":
            result.pop()
        else:
            free_index = result.index(".")
            result[free_index] = result.pop()
        # print(result)

    while len(result) < len(input):
        result.append(".")

    # print(result)

    return "".join(result)


def compute_checksum(input: str) -> int:
    total = 0

    for i, letter in enumerate(input):
        if letter == ".":
            continue
        total += i * int(letter)

    return total

def part_1():
    disk_map = parse_memory_block(INPUT)
    # print(disk_map)
    compressed = compress_block(disk_map)
    print(compute_checksum(compressed))


if __name__ == "__main__":
    part_1()
