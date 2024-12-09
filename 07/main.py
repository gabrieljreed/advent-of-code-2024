from pathlib import Path
import itertools

INPUT_FILE = Path(__file__).parent / "input.txt"
with open(INPUT_FILE, "r") as f:
    input = f.read()


test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

test_input_2 = "292: 11 6 16 20"

INPUT = input


def split_equation(input: str):
    result, operands = input.split(":")
    operands = operands.split()

    result = int(result)
    operands = [int(operand) for operand in operands]
    return result, operands


def add(x, y):
    return x + y

def mul(x, y):
    return x * y

def combine(x, y):
    return int(f"{x}{y}")


def get_operation_possibilities(operands: list[int]):
    # return list(itertools.product([add, mul], repeat=len(operands) - 1))
    return list(itertools.product([add, mul, combine], repeat=len(operands) - 1))


def test_equation(operands: list[int], result: int, verbose: bool = False) -> bool:
    possibility = (add, mul, add)
    for possibility in get_operation_possibilities(operands):
        prev = operands[0]
        for operand, operation in zip(operands[1:], possibility):
            operation_str = "+" if operation == add else "*"
            output_str = f"{prev} {operation_str} {operand} = "
            prev = operation(prev, operand)
            output_str += str(prev)
            if verbose:
                print(output_str)
        if verbose:
            print(prev)
        if prev == result:
            return True
    return False


if __name__ == "__main__":
    total = 0
    for line in INPUT.splitlines():
        result, operands = split_equation(line)
        valid = test_equation(operands, result, verbose=False)
        if valid:
            total += result

    print(total)

