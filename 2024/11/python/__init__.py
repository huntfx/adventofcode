"""Day 11: Plutonian Pebbles
https://adventofcode.com/2024/day/11
"""

from pathlib import Path


BASE = Path(__file__).parent.parent

TESTS_DIR = BASE / 'test-data'

CACHE: dict[tuple[int, int], int] = {}


def read_input(test: int = 0) -> list[int]:
    """Read the input.txt file.

    Returns:
        List of integers to represent the stones.
    """
    if test:
        path = TESTS_DIR / str(test) / 'input.txt'
    else:
        path = BASE / 'input.txt'

    with open(path, 'r') as f:
        return [int(val.strip('\r\n')) for val in f.read().split()]


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
                count, expected = map(int, line.split(':'))
                actual = fn(test_num, count)

                # Notify the user or raise an error
                if actual == expected:
                    print(f'Test {test_num} part {part_num} passed')
                else:
                    raise RuntimeError(f'Test {test_num} part {part_num} failed (expected {expected}, got {actual})')


def blink_individual(stone: int) -> list[int]:
    """Calculate the new state of the stone after a blink.

    >>> blink_individual(0)
    [1]
    >>> blink_individual(1000)
    [10, 0]
    >>> blink_individual(1)
    [2024]
    >>> blink_individual(11)
    [1, 1]
    """
    # If a stone is engraved with the number 0, it is replaced by a 1
    if stone == 0:
        return [1]

    # If a stone is engraved with a number that has an even number of
    # digits, it is replaced by two stones split down the middle
    string = str(stone)
    length = len(string)
    if not length % 2:
        return [int(string[:length // 2]), int(string[length // 2:])]

    # The stone's number multiplied by 2024 is engraved on the new stone
    return [stone * 2024]


def blink(*stones: int) -> list[int]:
    """Get the new list of stones.

    >>> blink(125, 17)
    [253000, 1, 7]
    >>> blink(253000, 1, 7)
    [253, 0, 2024, 14168]
    >>> blink(253, 0, 2024, 14168)
    [512072, 1, 20, 24, 28676032]
    >>> blink(512072, 1, 20, 24, 28676032)
    [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    >>> blink(512, 72, 2024, 2, 0, 2, 4, 2867, 6032)
    [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
    >>> blink(1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32)
    [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]
    """
    result = []
    for stone in stones:
        result.extend(blink_individual(stone))
    return result


def blink_multiple(stones: list[int], count: int) -> list[int]:
    """Get the new list of stones after multiple blinks.

    >>> blink_multiple([125, 17], 1)
    [253000, 1, 7]
    >>> blink_multiple([125, 17], 2)
    [253, 0, 2024, 14168]
    >>> blink_multiple([125, 17], 3)
    [512072, 1, 20, 24, 28676032]
    """
    for _ in range(count):
        stones = blink(*stones)
    return stones


def blink_multiple_count(stones: list[int], count: int) -> int:
    """Get the count of stones after multiple blinks.
    This is the optimised version to work with larger counts.

    >>> blink_multiple_count([125, 17], 1)
    3
    >>> blink_multiple_count([125, 17], 2)
    4
    >>> blink_multiple_count([125, 17], 3)
    5
    """
    if count == 1:
        return len(blink(*stones))

    total = 0
    for stone in stones:
        if (stone, count) not in CACHE:
            CACHE[(stone, count)] = blink_multiple_count(blink_individual(stone), count - 1)
        total += CACHE[(stone, count)]
    return total


def part_1(test: int = 0, count: int = 25) -> int:
    """Get the solution to part 1."""
    stones = read_input(test)
    return len(blink_multiple(stones, count))


def part_2(test: int = 0, count: int = 75) -> int:
    """Get the solution to part 2."""
    stones = read_input(test)
    return blink_multiple_count(stones, count)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
