"""Day 8: Resonant Collinearity
https://adventofcode.com/2024/day/8
"""

from pathlib import Path
from typing import Iterator
import numpy as np


BASE = Path(__file__).parent.parent

TESTS_DIR = BASE / 'test-data'


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


def load_map(test: int = 0) -> np.ndarray:
    """Load the input into a 2D array for the map."""
    return np.array([list(line) for line in read_input(test)])


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
            actual = fn(test_num)
            expected = int(output.read_text())

            # Notify the user or raise an error
            if actual == expected:
                print(f'Test {test_num} part {part_num} passed')
            else:
                raise RuntimeError(f'Test {test_num} part {part_num} failed (expected {expected}, got {actual})')


def iter_antenna_pairs(data: np.ndarray) -> Iterator[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Find matching antenna pairs on the same frequency.

    Generates:
        3 tuples: coordinates of the two antennas and their difference.
    """
    antennas_y, antennas_x = np.where(data != '.')
    antennas_coords = {*zip(antennas_y, antennas_x)}
    seen = set()
    for antenna_coord in antennas_coords:
        seen.add(antenna_coord)
        for pair_coord in antennas_coords - seen:
            if data[antenna_coord] == data[pair_coord]:
                diff = tuple(pair_coord[i] - antenna_coord[i] for i in range(2))
                yield antenna_coord, pair_coord, diff


def coordinate_valid(data: np.ndarray, coordinate: tuple[int, int]) -> bool:
    """Determine if a coordinate is valid for a given 2D array."""
    return 0 <= coordinate[0] < data.shape[0] and 0 <= coordinate[1] < data.shape[1]


def part_1(test: int = 0) -> int:
    """Calculate how many antinodes exist in the map."""
    antenna_map = load_map(test)

    antinodes = set()
    for (start_y, start_x), (end_y, end_x), (diff_y, diff_x) in iter_antenna_pairs(antenna_map):
        for antinode in ((start_y - diff_y, start_x - diff_x), (end_y + diff_y, end_x + diff_x)):
            if coordinate_valid(antenna_map, antinode):
                antinodes.add(antinode)

    return len(antinodes)


def part_2(test: int = 0) -> int:
    """Recalculate the antinodes based on harmonics.

    Antinodes occur at any grid position exactly in line with at least
    two antennas of the same frequency, regardless of distance. This
    means that some antinodes will occur at the position of each antenna.
    """
    antenna_map = load_map(test)

    antinodes = set()
    for (start_y, start_x), (end_y, end_x), (diff_y, diff_x) in iter_antenna_pairs(antenna_map):
        # Follow the resonant harmonics to the start of the map
        current_y, current_x = start_y, start_x
        while coordinate_valid(antenna_map, (current_y, current_x)):
            current_y += diff_y
            current_x += diff_x

        # Bring the coordinates in bounds
        current_y -= diff_y
        current_x -= diff_x

        # Calculate all the possible harmonics
        while coordinate_valid(antenna_map, (current_y, current_x)):
            antinodes.add((current_y, current_x))
            current_y -= diff_y
            current_x -= diff_x

    return len(antinodes)


if __name__ == '__main__':
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
