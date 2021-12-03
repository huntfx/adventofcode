"""Day 2: Dive!
https://adventofcode.com/2021/day/2
"""

from typing import Callable, Dict, List


def load_input(test: bool = False) -> List[str]:
    """Read the input.txt file.

    Returns:
        List of each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        return [line.strip('\r\n') for line in f]


def move(directions: Dict[str, Callable], test: bool = False) -> int:
    """Move the submarine according to the result of direction functions."""
    pos = [0, 0, 0]
    for line in load_input(test=test):
        direction, units = line.split()
        pos = directions[direction](pos, int(units))
    return pos[0] * pos[1]


def part_1(test: bool = False) -> int:
    """Move the submarine with horizontal and depth."""
    directions: Dict[str, Callable] = dict(
        up=lambda pos, units: [pos[0], pos[1] - units],
        down=lambda pos, units: [pos[0], pos[1] + units],
        forward=lambda pos, units: [pos[0] + units, pos[1]],
        backward=lambda pos, units: [pos[0] - units, pos[1]],
    )
    return move(directions, test=test)


def part_2(test: bool = False) -> int:
    """Move the submarine with horizontal, depth and aim."""
    directions: Dict[str, Callable] = dict(
        up = lambda pos, units: pos[:2] + [pos[2] - units],
        down = lambda pos, units: pos[:2] + [pos[2] + units],
        forward = lambda pos, units: [pos[0] + units, pos[1] + pos[2] * units, pos[2]],
        backward=lambda pos, units: [pos[0] - units] + pos[1:],
    )
    return move(directions, test=test)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 150


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 900


print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
