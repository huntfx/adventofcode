"""Day 10: Syntax Scoring
https://adventofcode.com/2021/day/10
"""

from functools import reduce
from typing import Dict, Generator, List, Tuple


# Scoring mapping for part 1
PART_1_SCORING = {')': 3, ']': 57, '}': 1197, '>': 25137}

# Scoring mapping for part 2
PART_2_SCORING = {')': 1, ']': 2, '}': 3, '>': 4}

# Mapping to find the correct closing replacement
CLOSING_REPLACE: Dict[str, str] = dict(('<>', '{}', '()', '[]'))


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def sort_lines(test: bool = False) -> Tuple[List[str], List[str]]:
    """Get "corrupted" and "incomplete" line data.

    Returns:
        List of corrupted characters, and a list of incomplete chunks.
    """
    corrupted = []
    incomplete = []
    for line in load_input(test=test):
        stack = []

        # Corrupted
        for x in reversed(line):
            if x in '>])}':
                stack.append(x)
            elif x in '<[({' and stack:
                invalid = stack.pop()
                if CLOSING_REPLACE[x] != invalid:
                    corrupted.append(invalid)
                    break

        # Incomplete
        else:
            for x in line:
                if x in '<[({':
                    stack.append(x)
                elif x in '>])}':
                    stack.pop()
            incomplete.append(''.join(map(CLOSING_REPLACE.get, reversed(stack))))

    return corrupted, incomplete


def part_1(test: bool = False) -> int:
    """Get the total syntax error score."""
    corrupted, incomplete = sort_lines(test=test)
    return sum(map(PART_1_SCORING.get, corrupted))


def part_2(test: bool = False) -> int:
    """Get the incomplete line score winner."""
    corrupted, incomplete = sort_lines(test=test)
    scores = [reduce(lambda a, b: a * 5 + PART_2_SCORING[b], x, 0) for x in incomplete]
    return list(sorted(scores))[len(scores) // 2]


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 26397


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 288957


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
