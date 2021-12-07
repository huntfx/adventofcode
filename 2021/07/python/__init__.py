"""Day 7: The Treachery of Whales
https://adventofcode.com/2021/day/7
"""

from typing import Generator


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def get_positions(test: bool=False) -> Generator[int, None, None]:
    """Get all the crab positions."""
    yield from map(int, next(load_input(test=test)).split(','))


def part_1(test: bool = False) -> int:
    """Get the linear shortest distance."""
    positions = list(get_positions(test=test))
    fn = lambda val: sum(abs(pos - val) for pos in positions)
    return min(map(fn, range(min(positions), max(positions) + 1)))


def part_2(test: bool = False) -> int:
    """Get the triangular shortest distance."""
    positions = list(get_positions(test=test))
    fn = lambda val: sum(n * (n + 1) // 2 for n in (abs(pos - val) for pos in positions))
    return min(map(fn, range(min(positions), max(positions) + 1)))


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 37


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 168


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
