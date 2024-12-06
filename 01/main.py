with open("01/input.txt") as f:
    lines = f.readlines()

left = []
right = []
for line in lines:
    l, r = line.split()
    left.append(l)
    right.append(r)

left.sort()
right.sort()

def part_1() -> int:
    total_difference = 0
    for l, r, in zip(left, right):
        difference = abs(int(l) - int(r))
        total_difference += difference

    return total_difference


def part_2() -> int:
    total = 0

    for number in left:
        count = len([i for i in right if i == number])
        number = int(number)
        total += number * count

    return total


if __name__ == "__main__":
    part_1_answer = part_1()
    print(part_1_answer)

    part_2_answer = part_2()
    print(part_2_answer)

