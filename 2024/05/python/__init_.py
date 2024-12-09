"""Day 5: Print Queue
https://adventofcode.com/2024/day/5
"""

from collections import defaultdict
from typing import Dict, Iterator, List, Set, Tuple


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def parse_input(test: bool = False) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    """Parse the input text.

    Returns:
        Order dict and updates.
    """
    ordering = defaultdict(set)
    section = 0
    updates = []
    for line in read_input(test):
        if not line:
            section += 1
            continue

        if section == 0:
            before, after = map(int, line.split('|'))
            ordering[after].add(before)
        elif section == 1:
            updates.append(list(map(int, line.split(','))))

    return ordering, updates


def verify_update(ordering: Dict[int, Set[int]], update: List[int]):
    """Verify if an update is valid or not.
    A valid update adheres to the correct page order.
    """
    for i, page in enumerate(update):
        remaining = ordering[page]
        after = update[i:]
        if set(remaining) & set(after):
            return 0
    return 1


def part_1(test: bool = False) -> int:
    """Count the middle pages of valid inputs."""
    ordering, updates = parse_input(test)
    valid = [update for update in updates if verify_update(ordering, update)]
    return sum(update[len(update) // 2] for update in valid)


def part_2(test: bool = False) -> int:
    """Count the middle pages of fixed invalid inputs."""
    ordering, updates = parse_input(test)
    invalid = [update for update in updates if not verify_update(ordering, update)]

    total = 0
    for update in invalid:
        size = len(update)

        # Keep iterating over the full update until no fixes are made
        while True:
            for i in range(1, size):
                current_page = update[i]
                previous_page = update[i - 1]

                # If the current page is not valid, swap it with the previous page
                valid_pages = ordering[current_page]
                if previous_page not in valid_pages:
                    update = update[:i - 1] + [current_page, previous_page] + update[i + 1:]
                    break
            else:
                break
        total += update[size // 2]
    return total


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 143


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 123


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')

