"""Day 7: Bridge Repair
https://adventofcode.com/2024/day/7
"""

import itertools
from typing import Iterator, Callable
import operator


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def parse_input(test: bool = False) -> list[tuple[int, list[int]]]:
    """Get the value and numbers from the input data.

    Returns:
        List of tuples containing (values, list of numbers).
    """
    results = []
    for line in read_input(test):
        value, numbers = line.split(': ')
        results.append((int(value), list(map(int, numbers.split()))))
    return results


def is_valid(value: int, numbers: list[int], ops: list[Callable]) -> bool:
    """Determine if a sequence of numbers is valid."""
    for combination in itertools.product(ops, repeat=len(numbers)-1):
        total = numbers[0]
        for i, op in enumerate(combination, 1):
            total = op(total, numbers[i])
            if total == value:
                return True
            if total > value:
                break
    return False


def part_1(test: bool = False) -> int:
    """Determine which numbers are valid with add and multiply."""
    data = parse_input(test)
    ops = [operator.add, operator.mul]
    return sum(value for value, numbers in data if is_valid(value, numbers, ops))


def part_2(test: bool = False) -> int:
    """Determine which numbers are valid with add/multiply/concatenate."""
    data = parse_input(test)
    ops = [operator.add, operator.mul, lambda a, b: int(f'{a}{b}')]
    return sum(value for value, numbers in data if is_valid(value, numbers, ops))


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 3749


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 11387


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
