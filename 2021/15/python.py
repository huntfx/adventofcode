"""Day 15: Chiton
https://adventofcode.com/2021/day/15
"""

import numpy as np
from typing import Generator


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def build_matrix(test: bool = False) -> np.ndarray:
    """Convert the input to a matrix of ints."""
    lines = list(map(list, load_input(test=test)))
    return np.array(lines, dtype=int)


def dijkstras_algorithm(matrix: np.ndarray) -> float:
    """Find the shortest path from the top left to the bottom right.

    Source: https://levelup.gitconnected.com/dijkstras-shortest-path-algorithm-in-a-grid-eb505eb3a290
    """
    max_x, max_y = matrix.shape

    # Initialize auxiliary arrays
    distmap = np.ones(matrix.shape, dtype=int) * np.Infinity
    distmap[0, 0] = 0
    originmap = np.ones(matrix.shape, dtype=int) * np.nan
    visited = np.zeros(matrix.shape, dtype=bool)
    x = y = 0

    # Loop Dijkstra until reaching the target cell
    while True:
        # Move to x+1, y
        if x < max_x - 1:
            if distmap[x+1, y] > matrix[x+1, y] + distmap[x, y] and not visited[x+1, y]:
                distmap[x+1, y] = matrix[x+1, y] + distmap[x, y]
                originmap[x+1, y] = np.ravel_multi_index([x, y], matrix.shape)
        # Move to x-1, y
        if x > 0:
            if distmap[x-1, y] > matrix[x-1, y] + distmap[x, y] and not visited[x-1, y]:
                distmap[x-1, y] = matrix[x-1, y] + distmap[x, y]
                originmap[x-1, y] = np.ravel_multi_index([x, y], matrix.shape)
        # Move to x, y+1
        if y < max_y - 1:
            if distmap[x, y+1] > matrix[x, y+1] + distmap[x, y] and not visited[x, y+1]:
                distmap[x, y+1] = matrix[x, y+1] + distmap[x, y]
                originmap[x, y+1] = np.ravel_multi_index([x, y], matrix.shape)
        # Move to x, y-1
        if y > 0:
            if distmap[x, y-1] > matrix[x, y-1] + distmap[x, y] and not visited[x, y-1]:
                distmap[x, y-1] = matrix[x, y-1] + distmap[x, y]
                originmap[x, y-1] = np.ravel_multi_index([x, y], matrix.shape)

        visited[x, y] = True
        dismaptemp = distmap
        dismaptemp[np.where(visited)] = np.Infinity

        # Find the shortest path so far
        x, y = np.unravel_index(np.argmin(dismaptemp), dismaptemp.shape)
        if x == max_x-1 and y == max_y-1:
            break

    return distmap[max_x-1, max_y-1]


def increment_matrix(matrix: np.ndarray) -> np.ndarray:
    """Add 1 to the matrix, and wrap to 1 if any value reaches 10."""
    return (matrix % 9) + 1


def part_1(test: bool = False) -> int:
    """Get the total risk of the path."""
    return int(dijkstras_algorithm(build_matrix(test=test)))


def part_2(test: bool = False) -> int:
    """Get the total risk of the path when the matrix is 5x larger.
    Each adjacent copy of the matrix is 1 higher than the previous.
    """
    top_left = build_matrix(test=test)

    rows = [top_left]
    for _ in range(4):
        rows.append(increment_matrix(rows[-1]))
    row = np.concatenate(rows, axis=0)

    columns = [row]
    for _ in range(4):
        columns.append(increment_matrix(columns[-1]))
    matrix = np.concatenate(columns, axis=1)

    return int(dijkstras_algorithm(matrix))


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 40


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 315


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
