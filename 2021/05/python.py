"""Day 5: Hydrothermal Venture
https://adventofcode.com/2021/day/5
"""

import numpy as np
from typing import Generator, List, Tuple, Union


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def parse_input(test: bool = False) -> Generator[Tuple[Tuple[int, int], Tuple[int, int]], None, None]:
    """Read the input and convert to coordinates."""
    for line in load_input(test=test):
        start, end = line.split(' -> ')
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, end.split(','))
        yield ((x1, y1), (x2, y2))


def range_override(a: int, b: int) -> Union[List[int], range]:
    """Get the correct range for the vent data."""
    step = (-1, 1)[a <= b]
    if a == b:
        return [a]
    return range(a, b + step, 1 if a < b else step)


def build_vents(diagonal: bool = True, test: bool = False) -> np.ndarray:
    """Build the grid of vents."""
    vents = list(parse_input(test=test))

    # Find the area size
    top_left = [float('inf')] * 2
    bottom_right = [-float('inf')] * 2
    for (x1, y1), (x2, y2) in vents:
        top_left = [min(top_left[0], x1, x2), min(top_left[1], y1, y2)]
        bottom_right = [max(bottom_right[0], x1, x2), max(bottom_right[1], y1, y2)]

    grid = np.zeros((bottom_right[0] - top_left[0] + 1, bottom_right[1] - top_left[1] + 1), dtype=int)
    for i, ((x1, y1), (x2, y2)) in enumerate(vents):
        # Horizontal
        if x1 == x2 or y1 == y2:
            if test:
                print(f'{i}: Horizontal ({x1, y1} -> {x2, y2})')
            for x in range_override(x1, x2):
                for y in range_override(y1, y2):
                    grid[x - top_left[0], y - top_left[1]] += 1

        # Diagonal
        elif diagonal and abs(x1 - x2) == abs(y1 - y2):
            if test:
                print(f'{i}: Diagonal ({x1, y1} -> {x2, y2})')
            for x, y in zip(range_override(x1, x2), range_override(y1, y2)):
                grid[x - top_left[0], y - top_left[1]] += 1

        # Unknown
        elif test:
            print(f'{i}: Invalid ({x1, y1} -> {x2, y2})')

    return np.fliplr(np.rot90(grid, 3))


def part_1(test: bool = False) -> int:
    """Find all the horizontal overlaps."""
    grid = build_vents(False, test=test)
    return np.count_nonzero(grid > 1)


def part_2(test: bool = False) -> int:
    """Find all the horizontal and vertical overlaps."""
    grid = build_vents(True, test=test)
    return np.count_nonzero(grid > 1)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 5


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 12


if __name__ == '__main__':
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
