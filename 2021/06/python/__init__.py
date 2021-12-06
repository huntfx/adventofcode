"""Day 6: Lanternfish
https://adventofcode.com/2021/day/6
"""

from collections import Counter, defaultdict
from typing import Counter as CounterType, Dict, Generator, Union


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def get_fish(test: bool = False) -> CounterType[int]:
    """Get the fish from the input and count the ages."""
    return Counter(map(int, next(load_input(test=test)).split(',')))


def spawn_fish(days: int = 80, test: bool = False) -> int:
    """Count the number of fish after a number of days."""
    fish_counts: Union[Dict[int, int], CounterType[int]] = get_fish(test=test)
    for _ in range(days):
        fish_next: Dict[int, int] = defaultdict(int)
        for i, val in fish_counts.items():
            if i:
                fish_next[i - 1] += val
            else:
                fish_next[6] += val
                fish_next[8] += val
        fish_counts = fish_next
    return sum(fish_counts.values())


def part_1(days: int = 80, test: bool = False) -> int:
    """Get the fish numbers after 80 days."""
    return spawn_fish(days=days, test=test)


def part_2(days: int = 256, test: bool = False) -> int:
    """Get the fish numbers after 256 days."""
    return spawn_fish(days=days, test=test)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(18, test=True) == 26
    assert part_1(80, test=True) == 5934


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 26984457539


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
