from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"
SAFE_DISTANCE = 3

with open(INPUT_FILE, "r") as f:
    lines = f.readlines()


def is_report_safe(report: str, verbose: bool = False) -> bool:
    levels = report.split()

    if int(levels[0]) > int(levels[1]):
        is_decreasing = True
    else:
        is_decreasing = False

    for i in range(len(levels) - 1):
        current_level = int(levels[i])
        next_level = int(levels[i + 1])

        difference = abs(current_level - next_level)
        if difference > SAFE_DISTANCE:
            if verbose:
                print(f"{current_level}, {next_level} - distance {difference} too great")
            return False

        if difference == 0:
            if verbose:
                print(f"{current_level}, {next_level} - distance {difference} == 0")
            return False

        if is_decreasing and current_level < next_level:
            if verbose:
                print(f"{current_level}, {next_level} - report is DECREASING")
            return False

        if not is_decreasing and current_level > next_level:
            if verbose:
                print(f"{current_level}, {next_level} - report is INCREASING")
            return False

    return True


def get_report_one_level_removed(report: str) -> list[str]:
    reports = []

    levels = report.split()
    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i + 1:]
        reports.append(" ".join(new_levels))

    return reports


def part_1():
    num_safe_reports = 0
    for line in lines:
        line = line.strip()
        if is_report_safe(line, verbose=True):
            num_safe_reports += 1

    print(num_safe_reports)


def part_2():
    num_safe_reports = 0
    for line in lines:
        line = line.strip()
        if is_report_safe(line, verbose=True):
            num_safe_reports += 1
        else:
            # Try to make the report safe by removing a level
            reports_removed = get_report_one_level_removed(line)
            if any([is_report_safe(report) for report in reports_removed]):
                num_safe_reports += 1

    print(num_safe_reports)


if __name__ == "__main__":
    print(part_1())
    print(part_2())

