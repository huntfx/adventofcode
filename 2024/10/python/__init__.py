"""Day 10: Hoof It
https://adventofcode.com/2024/day/10
"""

from pathlib import Path
from typing import Iterator
import numpy as np


BASE = Path(__file__).parent.parent

TESTS_DIR = BASE / 'test-data'

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def read_input(test: int = 0) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    if test:
        path = TESTS_DIR / str(test) / 'input.txt'
    else:
        path = BASE / 'input.txt'

    with open(path, 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def load_data(test: int = 0) -> np.ndarray[str, np.dtype.str]:
    """Load the input into a 2D array."""
    return np.array([list(line) for line in read_input(test)])


def find_trails(array: np.ndarray) -> list[list[tuple[int, int]]]:
    """Find all the hiking trails from the lowest to highest points.
    A path must start at height 0, end at height 9, and only increase
    in increments of 1. It'll never go diagonal.
    """
    coordinates = [np.where(array == str(n)) for n in range(10)]
    possible_paths = [[[(int(x), int(y))] for x, y in zip(*coordinates[0])]]

    # Step through each height
    for x_coords, y_coords in coordinates[1:]:
        current_paths: list[list[tuple[int, int]]] = []
        previous_paths = possible_paths[-1]
        possible_paths.append(current_paths)

        # Check each possible direction
        for x, y in zip(x_coords, y_coords):
            # Check each ongoing path
            for path in previous_paths:
                for dx, dy in DIRECTIONS:
                    # If the direction is valid, append that as a new trail
                    if path[-1] == (x + dx, y + dy):
                        current_paths.append(path + [(x, y)])

    # Return the paths at height 9
    return possible_paths[-1]


def run_tests() -> None:
    """Run test data to ensure the results are as expected.

    Raises:
        RuntimeError: If any test fails
    """
    for test_folder in TESTS_DIR.iterdir():
        test_num = int(test_folder.name)

        for fn in (part_1, part_2):
            # Check for output file
            part_num = fn.__name__.split('_')[-1]
            output = test_folder / f'output-part{part_num}.txt'
            if not output.exists():
                continue

            # Get the actual vs expected result
            actual = fn(test_num)
            expected = int(output.read_text())

            # Notify the user or raise an error
            if actual == expected:
                print(f'Test {test_num} part {part_num} passed')
            else:
                raise RuntimeError(f'Test {test_num} part {part_num} failed (expected {expected}, got {actual})')


def part_1(test: int = 0) -> int:
    """Get the trail score for a map."""
    data = load_data(test)
    trails = find_trails(data)
    return len({(path[0], path[-1]) for path in trails})


def part_2(test: int = 0) -> int:
    """Get the trail rating for a map."""
    data = load_data(test)
    trails = find_trails(data)
    return len(trails)


if __name__ == '__main__':
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
