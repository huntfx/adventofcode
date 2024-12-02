from typing import Iterator, List


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def load_data(test: bool = False):
    """Load the data in the required format."""
    result = []
    for line in read_input(test):
        levels = map(int, line.split())
        result.append(list(levels))
    return result


def is_safe(levels: List[int]) -> bool:
    """Determine if a levels reading is safe.

    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    """
    increasing = levels[0] < levels[-1]

    # Check they are increasing/decreasing
    levels_sorted = list(sorted(levels))
    if not increasing:
        levels_sorted.reverse()
    if levels != levels_sorted:
        return False

    # Check the difference between each number
    pairs = zip(levels[:-1], levels[1:])
    diffs = [abs(i - j) for i, j in pairs]
    return 1 <= min(diffs) and max(diffs) <= 3


def part_1(test: bool = False) -> int:
    """Count how many levels are safe."""
    return sum(is_safe(levels) for levels in load_data(test))


def part_2(test: bool = False) -> int:
    """Count how many levels are within tolerance."""
    count = 0
    for levels in load_data(test):
        count += 1
        for i in range(len(levels) + 1):
            if is_safe(levels[:i - 1] + levels[i:]) if i else is_safe(levels):
                break
        else:
            count -= 1
    return count


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 2


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 4


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
