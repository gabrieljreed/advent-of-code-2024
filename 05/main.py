from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"
with open(INPUT_FILE, "r") as f:
    input = f.read()

test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

rules_registry = {}


class Rule:
    def __init__(self, page: str):
        self.page = page
        self.pages_before = []
        self.pages_after = []

    def __str__(self):
        result = f"Page: {self.page}\n"
        result += f"\tPages before: {self.pages_before}\n"
        result += f"\tPages after: {self.pages_after}"
        return result


def parse_rules(rules: list[str]):
    for rule in rules:
        before, after = rule.split("|")
        rule_before = rules_registry.get(before, Rule(before))
        rule_after = rules_registry.get(after, Rule(after))
        rule_before.pages_after.append(after)
        rule_after.pages_before.append(before)
        rules_registry[before] = rule_before
        rules_registry[after] = rule_after


def check_update(update: str, verbose: bool = False) -> bool:
    pages = update.split(",")
    for i, page in enumerate(pages):
        page_rule = rules_registry.get(page)
        if not page_rule:
            continue

        previous_pages = pages[:i]
        next_pages = pages[i + 1:]

        for page_before in page_rule.pages_before:
            if page_before in next_pages:
                if verbose:
                    print(f"Update {update} violates {page_before}|{page}")
                return False

        for page_after in page_rule.pages_after:
            if page_after in previous_pages:
                if verbose:
                    print(f"Update {update} violates {page}|{page_after}")
                return False

    return True


def get_middle_page_number(update: str):
    pages = update.split(",")
    return pages[len(pages) // 2]


"""
75,97,47,61,53 violates the rules 97|75

75,97,47,61,53 becomes 97,75,47,61,53
"""
def fix_update(update: str) -> str:
    fixed = False

    pages = update.split(",")

    while not fixed:
        for i in range(len(pages)):
            page = pages[i]
            page_rule = rules_registry[page]

            previous_pages = pages[:i]
            next_pages = pages[i + 1:]

            for page_before in page_rule.pages_before:
                # Check if a page appears after a page it's supposed to appear before
                if page_before in next_pages:
                    index_before = pages.index(page_before)
                    # Can't just use `i` here, because the page might've already been moved during this iteration
                    index_after = pages.index(page)  
                    pages[index_before] = page
                    pages[index_after] = page_before

            fixed = check_update(",".join(pages))

    return ",".join(pages)


def split_input_text(text: str) -> tuple[list[str], list[str]]:
    """Split input text into rules and updates."""
    lines = text.splitlines()

    rules: list[str] = []
    updates: list[str] = []

    is_rules = True

    for line in lines:
        if line.strip() == "":
            is_rules = False
            continue
        if is_rules:
            rules.append(line)
        else:
            updates.append(line)

    return rules, updates


def part_1():
    rules, updates = split_input_text(input)
    # print(f"{rules = }")
    # print(f"{updates = }")

    parse_rules(rules)
    # for rule in rules_registry.values():
    #     print(rule)

    total = 0
    for update in updates:
        if not check_update(update):
            continue
        # print(update, check_update(update, verbose=True))
        total += int(get_middle_page_number(update))

    print(total)


def part_2():
    rules, updates = split_input_text(input)
    parse_rules(rules)

    total = 0
    for update in updates:
        if check_update(update):
            continue
        fixed_update = fix_update(update)
        total += int(get_middle_page_number(fixed_update))

    print(total)


if __name__ == "__main__":
    # part_1()
    part_2()

