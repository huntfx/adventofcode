"""Day 14: Extended Polymerization"""

from collections import Counter
from typing import Dict, Generator, Tuple


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def parse_input(test: bool = False) -> Tuple[str, Dict[str, str]]:
    """Convert the input to the template and replacements."""
    lines = list(load_input(test))
    template = lines[0]
    replacement = dict(line.split(' -> ') for line in lines[2:])
    return template, replacement


def polymerize(steps: int, test: bool = False) -> int:
    """Run the polymerization.

    Returns:
        Difference between the quantity of the most and least common elements.
    """
    template, replacement = parse_input(test=test)

    counts = Counter(template)
    pairs = Counter((template[i: i + 2] for i in range(len(template) - 1)))
    for step in range(steps):
        for pair, count in dict(pairs).items():
            mid = replacement[pair]
            counts[mid] += count
            pairs[pair] -= count
            pairs[pair[0] + mid] += count
            pairs[mid + pair[1]] += count

    least_common = min(counts, key=counts.get)
    most_common = max(counts, key=counts.get)
    return counts[most_common] - counts[least_common]



def part_1(test: bool = False) -> int:
    """Get the total syntax error score."""
    return polymerize(10, test=test)


def part_2(test: bool = False) -> int:
    """Get the incomplete line score winner."""
    return polymerize(40, test=test)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 1588


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 2188189693529


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
