from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent / "input.txt"
with open(INPUT_FILE, "r") as f:
    lines = f.readlines()

MUL_PATTERN = r"mul\((\d{1,3},\d{1,3})\)"
ENABLE_PATTERN = r"do\(\)"
DISABLE_PATTERN = r"don't\(\)"


def part_1():
    total = 0

    for line in lines:
        matches = re.findall(MUL_PATTERN, line)
        for match in matches:
            a, b = match.split(",")
            total += int(a) * int(b)

    return total


def part_2():
    enabled = True
    total = 0
    combined_pattern = f"{MUL_PATTERN}|{ENABLE_PATTERN}|{DISABLE_PATTERN}"

    for line in lines:
        for match in re.finditer(combined_pattern, line):
            found_string = match.group(0)
            if found_string == "do()":
                enabled = True
            elif found_string == "don't()":
                enabled = False
            elif enabled:
                matches = re.findall(MUL_PATTERN, found_string)
                for new_match in matches:
                    a, b = new_match.split(",")
                    total += int(a) * int(b)

    return total

if __name__ == "__main__":
    print(part_1())
    print(part_2())

