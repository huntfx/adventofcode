"""Day 9: Smoke Basin
https://adventofcode.com/2021/day/9
"""

import math
import numpy as np
from functools import partial
from typing import Generator, List, Tuple


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def generate_matrix(test: bool = False) -> np.ndarray:
    """Convert the input into a matrix."""
    lines = list(map(list, load_input(test=test)))
    return np.array(lines, dtype=int)


def get_adjacent(matrix, coordinate: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    """Get the valid adjancent coordinates to a coordinate."""
    range_x = range(0, matrix.shape[0])
    range_y = range(0, matrix.shape[1])
    for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        if coordinate[0] + x in range_x and coordinate[1] + y in range_y:
            yield (coordinate[0] + x, coordinate[1] + y)


def find_if_low(matrix: np.ndarray, coordinate: Tuple[int, int]) -> bool:
    """Determine if a point is a low point."""
    for adjancent in get_adjacent(matrix, coordinate):
        if matrix[adjancent] <= matrix[coordinate]:
            return False
    return True


def find_low(matrix: np.ndarray) -> Generator[List[int], None, None]:
    """Find the low points of a matrix.
    A low point is surrounded by higher points in the x and y directions.
    """
    yield from filter(partial(find_if_low, matrix), np.ndindex(matrix.shape))


def flood_fill(matrix: np.ndarray, coordinate: Tuple[int, int], fill=None):
    """Fill in the matrix until values of 9 are found."""
    if fill is None:
        fill = np.zeros(matrix.shape, dtype=bool)

    # Coordinate already visited
    if fill[coordinate]:
        return fill

    # Recursively fill in adjancent coordinates
    fill[coordinate] = True
    for adjancent in get_adjacent(matrix, coordinate):
        if matrix[adjancent] == 9:
            continue
        flood_fill(matrix, adjancent, fill)
    return fill


def part_1(test: bool = False) -> int:
    """Find the risk level.
    This is calculated by the height of the lowest point + 1.
    """
    matrix = generate_matrix(test=test)
    return sum(matrix[coordinate] + 1 for coordinate in find_low(matrix))


def part_2(test: bool = False) -> int:
    """Find the 3 largest basins.
    A basin is surrounded by a height of 9.
    """
    matrix = generate_matrix(test=test)
    basin_sizes = map(np.sum, map(partial(flood_fill, matrix), find_low(matrix)))
    largets_basins = list(sorted(basin_sizes))[-3:]
    return math.prod(largets_basins)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 15


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 1134


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
