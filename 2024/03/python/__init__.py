"""Day 3: Mull It Over
https://adventofcode.com/2024/day/3
"""

import re
import math
from typing import Iterator, List


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def read_memory(test: bool = False) -> str:
    """Load in the memory from the text file."""
    return ''.join(read_input(test))


def scan_memory(memory: str) -> int:
    """Find all the matching memory records.
    With the results, multiply each one then add them all together.
    """
    total = 0
    for match in re.findall(r'mul\((\d+,\d+)\)', memory):
        a, b = map(int, match.split(','))
        total += a * b
    return total


def filter_memory(memory: str) -> str:
    """Filter out memory blocks ignored by instructions.
    This removes anything between `don't()` and `do()`.
    """
    return re.sub("(don't\(\))(.*?)(do\(\))", '', memory)


def part_1(test: bool = False) -> int:
    """Count how many levels are safe."""
    return scan_memory(read_memory(test))


def part_2(test: bool = False) -> int:
    """Count how many levels are within tolerance."""
    return scan_memory(filter_memory(read_memory(test)))


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 161


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 48


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
