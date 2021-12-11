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


def get_adjacent(shape: Tuple[int, int], coordinate: Tuple[int, int],
                 ) -> Generator[Tuple[int, int], None, None]:
    """Get the valid adjancent coordinates to a coordinate."""
    for x, y in ((i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j):
        if 0 <= coordinate[0] + x < shape[0] and 0 <= coordinate[1] + y < shape[1]:
            yield (coordinate[0] + x, coordinate[1] + y)


def step(octopuses: np.ndarray) -> np.ndarray:
    """Charge each octopus by 1, and flash if it reaches 9.
    Adjenct octopuses will gain energy from a flash.
    If a flash occurs, then the octopus cannot gain energy again.

    Returns:
        Boolean array of where the flashes occurred.
    """
    flashed = np.zeros(octopuses.shape, dtype=bool)

    while np.any(octopuses >= 9):
        for x, y in np.ndindex(octopuses.shape):
            if octopuses[x, y] >= 9:
                octopuses[x, y] = 0
                flashed[x, y] = True
                rows, cols = zip(*get_adjacent(octopuses.shape, (x, y)))
                octopuses[rows, cols] += 1

    octopuses += 1
    octopuses[flashed] = 0
    return flashed


def part_1(test: bool = False) -> int:
    """Find the total number of flashes in 100 steps."""
    octopuses = generate_matrix(test=test)
    return sum(np.sum(step(octopuses)) for i in range(100))


def part_2(test: bool = False) -> int:
    """Find how many steps until everything flashes at once."""
    octopuses = generate_matrix(test=test)
    i = 1
    while not np.all(step(octopuses)):
        i += 1
    return i


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 1656


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 195


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
