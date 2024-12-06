from collections import defaultdict
from typing import Dict, Iterator, List, Set, Tuple
import numpy as np


DIRECTIONS = '^>v<^'


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


def guard_walk(array: np.ndarray) -> Tuple[int, str]:
    """Follow the walk the guard makes.
    Stops when they leave the room or enter a loop.
    """
    (cy,), (cx,) = np.where(np.isin(array, ('>', '^', '<', 'v')))
    direction = array[cy][cx]

    visited = set()
    while True:
        array[cy][cx] = 'X'
        while True:
            if direction == '^':
                next_coordinate = (cy - 1, cx)
            elif direction == '>':
                next_coordinate = (cy, cx + 1)
            elif direction == 'v':
                next_coordinate = (cy + 1, cx)
            elif direction == '<':
                next_coordinate = (cy, cx - 1)
            if not (0 <= next_coordinate[0] < array.shape[0] and 0 <= next_coordinate[1] < array.shape[1]):
                return array, 'exit'
            if array[next_coordinate] in ('.', 'X'):
                break
            if array[next_coordinate] == '#':
                direction = DIRECTIONS[DIRECTIONS.index(direction) + 1]

        visited_key = (next_coordinate, direction)
        if visited_key in visited:
            return array, 'loop'
        else:
            visited.add(visited_key)

        array[next_coordinate] = direction
        cy, cx = next_coordinate


def part_1(test: bool = False) -> int:
    """Count the number of positions visited by the guard."""
    floor = load_array(test)
    return np.sum(guard_walk(floor)[0] == 'X')


def part_2(test: bool = False) -> int:
    """Find how many loops are possible by adding 1 item."""
    floor = load_array(test)
    result = 0

    # Filter down the results to check
    visited = guard_walk(floor.copy())[0]
    check = (floor == '.') & (visited == 'X')

    # Test each new obstruction
    for y, x in zip(*np.where(check)):
        copy = floor.copy()
        copy[y][x] = '#'
        if guard_walk(copy)[1] == 'loop':
            result += 1
    return result


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 41


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 6


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
