"""Day 14: Restroom Redoubt
https://adventofcode.com/2024/day/14
"""

import math
import os
from itertools import count
from pathlib import Path
from typing import Iterator, Optional

import numpy as np
from scipy.special import entr
from PIL import Image


BASE = Path(__file__).parent.parent

TESTS_DIR = BASE / 'test-data'


def read_input(test: int = 0) -> Iterator[int]:
    """Read the input.txt file.

    Returns:
        List of integers to represent the stones.
    """
    if test:
        path = TESTS_DIR / str(test) / 'input.txt'
    else:
        path = BASE / 'input.txt'

    with open(path, 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def run_tests() -> None:
    """Run test data to ensure the results are as expected.

    Raises:
        RuntimeError: If any test fails.
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
            for line in output.read_text().strip().split('\n'):
                width, height, expected = map(int, line.split(':'))
                actual = fn(test_num, width, height)

                # Notify the user or raise an error
                if actual == expected:
                    print(f'Test {test_num} part {part_num} passed')
                else:
                    raise RuntimeError(f'Test {test_num} part {part_num} failed (expected {expected}, got {actual})')


def simulate_robot(p: tuple[int, int], v: tuple[int, int], w: int, h: int, n: int) -> tuple[int, int]:
    """Simulate where a robot will be after a number of seconds.

    Parameters:
        p: Position of robot.
        v: Velocity of robot.
        w: Width of area.
        h: Height of area.
        n: Number of seconds to simulate.

    Returns:
        New position of robot.
    """
    return (p[0] + v[0] * n) % w, (p[1] + v[1] * n) % h


def load_robots(test: bool = 0) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    """Load the initial state of robots from data.

    Yields:
        Tuple of position and velocity.
    """
    for line in read_input(test):
        p_str, v_str = line[2:].split(' v=')
        px, py = map(int, p_str.split(','))
        vx, vy = map(int, v_str.split(','))
        yield (px, py), (vx, vy)


def _to_array(positions: list[tuple[int, int]], width: int, height: int) -> np.ndarray:
    """Convert the robot positions to a numpy array."""
    array = np.zeros((height, width), dtype=int)
    array[:,:] = 0
    for x, y in positions:
        array[y, x] += 1
    return array


def calculate_safety_factor(positions: list[tuple[int, int]], width: int, height: int) -> int:
    """Calculate the safety factor of the robots.
    This is done by multiplying the count of robots per quadrant.
    Robots that are exactly in the middle don't count as being in any
    quadrant.
    """
    w_l = (0, width // 2 - 1)
    w_r = (math.ceil(width / 2), width)
    h_t = (0, height // 2 - 1)
    h_b = (math.ceil(height / 2), height)

    quadrant_counts = []
    for w1, w2 in (w_l, w_r):
        for y1, y2 in (h_t, h_b):
            quadrant_counts.append(sum(1 for x, y in positions if w1 <= x <= w2 and y1 <= y <= y2))
    return math.prod(quadrant_counts)


def calculate_entropy(positions: list[tuple[int, int]], width: int, height: int) -> float:
    """Calculate the entropy of a position of robots."""
    return entr(_to_array(positions, width, height)).sum()


def save_image(filename: str, positions: list[tuple[int, int]], width: int, height: int) -> None:
    """Save an image."""
    array = _to_array(positions, width, height)
    image_data = np.zeros(list(array.shape) + [3], dtype=np.uint8)
    for y in range(image_data.shape[0]):
        for x in range(image_data.shape[1]):
            val = array[y, x]
            if val == 0:
                image_data[y, x] = (255, 255, 255)
            elif val == 1:
                image_data[y, x] = (0, 0, 0)
            elif val == 2:
                image_data[y, x] = (255, 0, 0)
            elif val == 3:
                image_data[y, x] = (0, 0, 255)
            else:
                image_data[y, x] = (0, 255, 0)
    Image.fromarray(image_data).save(filename)


def part_1(test: bool = 0, width: int = 101, height: int = 103):
    """Calculate the safety factor after 100 seconds."""
    positions = [simulate_robot(p, v, width, height, 100) for p, v in load_robots(test)]
    return calculate_safety_factor(positions, width, height)


def part_2(test: bool = 0, width: int = 101, height: int = 103,
           use_entropy: bool = False, output_directory: Optional[str] = None):
    """Find the hidden christmas tree.

    This can work with either the safety factor or entropy.
    With the safety factor, the hidden tree is half that of the average.
    With entropy, an example value would be -13, and the tree is 0.

    >>> part_2(use_entropy=False) == part_2(use_entropy=True)
    True
    """
    # Load positions are velocities separately
    positions = []
    velocities = []
    for p, v in load_robots(test):
        positions.append(p)
        velocities.append(v)

    safety_factors = 0
    for i in count(1):
        # Update positions
        positions = [simulate_robot(p, v, width, height, 1) for p, v in zip(positions, velocities)]

        # Save image
        if output_directory is not None:
            save_image(os.path.join(output_directory, f'robots.{i}.jpg'), positions, width, height)

        # Calculate entropy
        if use_entropy:
            entropy = calculate_entropy(positions, width, height)
            if not entropy:
                return i

        # Calculate safety factor
        else:
            safety_factor = calculate_safety_factor(positions, width, height)
            safety_factors += safety_factor
            average_safety_factor = safety_factors / (i + 1)
            if safety_factor < average_safety_factor / 2:
                return i


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
