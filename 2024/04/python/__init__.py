"""Day 3: Mull It Over
https://adventofcode.com/2024/day/3
"""

import logging
import numpy as np
from typing import Iterator


logger = logging.getLogger()


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def load_array(test: bool) -> np.ndarray:
    """Load the input into a numpy array."""
    return np.array(list(map(list, read_input(test))))


def part_1(test: bool = False) -> int:
    """Count the occurances of XMAS in the word search.

    This word search allows words to be horizontal, vertical, diagonal,
    written backwards, or even overlapping other words.
    """
    search = list('XMAS')

    arr = load_array(test)
    height, width = arr.shape
    matches = 0
    for x in range(3, width):
        for y in range(height):
            if [arr[y][x - 3 + i] for i in range(4)] == search:
                logger.info('Found horizontal match going right: (%d, %d)', y, x - 3)
                matches += 1
            if [arr[y][x - i] for i in range(4)] == search:
                logger.info('Found horizontal match going left: (%d, %d)', y, x)
                matches += 1

    for x in range(width):
        for y in range(3, height):
            if [arr[y - 3 + i][x] for i in range(4)] == search:
                logger.info('Found vertical match going down: (%d, %d)', y - 3, x)
                matches += 1
            if [arr[y - i][x] for i in range(4)] == search:
                logger.info('Found vertical match going up: (%d, %d)', y, x)
                matches += 1

    for x in range(3, width):
        for y in range(3, height):
            if [arr[y - 3 + i][x - 3 + i] for i in range(4)] == search:
                logger.info('Found diagonal match going bottom right: (%d, %d)', y - 3, x - 3)
                matches += 1
            if [arr[y - i][x - i] for i in range(4)] == search:
                logger.info('Found diagonal match going top left: (%d, %d)', y, x)
                matches += 1
            if [arr[y - 3 + i][x - i] for i in range(4)] == search:
                logger.info('Found diagonal match going bottom left: (%d, %d)', y - 3, x)
                matches += 1
            if [arr[y - i][x - 3 + i] for i in range(4)] == search:
                logger.info('Found diagonal match going top right: (%d, %d)', y, x - 3)
                matches += 1

    return matches


def part_2(test: bool = False) -> int:
    """Search for two MAS in the shape of an X."""
    arr = load_array(test)
    check = set('MS')
    matches = 0
    for y, x in zip(*np.where(arr[1:-1,1:-1] == 'A')):
        if {arr[y][x], arr[y+2][x+2]} == {arr[y+2][x], arr[y][x+2]} == check:
            logger.info('Found X match: (%d, %d)', y, x)
            matches += 1
    return matches


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 18


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 9


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
