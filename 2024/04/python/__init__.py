"""Day 4: Ceres Search
https://adventofcode.com/2024/day/4
"""

import numpy as np
from typing import Iterator


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


def wordsearch(arr: np.ndarray, search: str) -> int:
    """Search an array for a word.
    All directions are supported.

    Parameters:
        arr: 2D character array.
        search: Case sensitive word to search for.

    Returns:
        The number of matches found.
    """
    matches = 0

    for rot in range(4):
        arr_rot = np.rot90(arr, rot)
        height, width = arr_rot.shape
        for x in range(3, width):
            for y in range(height):
                # Search to the left
                matches += all(arr_rot[y][x - i] == c for i, c in enumerate(search))

                # Search diagonal to the top left
                if y >= 3:
                    matches += all(arr_rot[y - i][x - i] == c for i, c in enumerate(search))
    return matches


def xsearch(arr: np.ndarray, search: str) -> int:
    """Search an array for an X word.

    Parameters:
        arr: 2D character array.
        search: 3 letter word to search that crosses in the middle.
            For example, MAS will search for:
                M.S
                .A.
                M.S

    Returns:
        The number of matches found.
    """
    try:
        left, middle, right = search
    except ValueError:
        raise ValueError('search must be exactly 3 characters')

    matches = 0
    for y, x in zip(*np.where(arr[1:-1,1:-1] == middle)):
        matches += {arr[y][x], arr[y+2][x+2]} == {arr[y+2][x], arr[y][x+2]} == {left, right}
    return matches


def part_1(test: bool = False) -> int:
    """Count the occurances of XMAS in the word search.

    This word search allows words to be horizontal, vertical, diagonal,
    written backwards, or even overlapping other words.
    """
    return wordsearch(load_array(test), 'XMAS')


def part_2(test: bool = False) -> int:
    """Search for two MAS in the shape of an X."""
    return xsearch(load_array(test), 'MAS')


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
