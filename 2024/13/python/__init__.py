from pathlib import Path
from typing import Iterator


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


def run_tests() -> None:
    """Run test data to ensure the results are as expected.

    Raises:
        RuntimeError: If any test fails.
    """
    for test_folder in TESTS_DIR.iterdir():
        test_num = int(test_folder.name)

        for fn in (part_1,):
            # Check for output file
            part_num = fn.__name__.split('_')[-1]
            output = test_folder / f'output-part{part_num}.txt'
            if not output.exists():
                continue

            # Get the answers
            expected = int(output.read_text())
            actual = fn(test_num)

            # Notify the user or raise an error
            if actual == expected:
                print(f'Test {test_num} part {part_num} passed')
            else:
                raise RuntimeError(f'Test {test_num} part {part_num} failed (expected {expected!r}, got {actual!r})')


def parse_input(test: int = 0) -> Iterator[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    """Parse the input data."""
    for i, line in enumerate(read_input(test)):
        idx = i % 4

        # Create a new result list for each claw machine
        if not idx:
            result: list[tuple[int, int]] = []

        # Send the data after the current machine has been read
        if idx == 3:
            yield (result[0], result[1], result[2])
            continue

        # Parse the data
        x, y = map(int, (x.replace('=', '+').split('+')[1] for x in line.split(': ')[1].split(', ')))
        result.append((x, y))


def calculate_cost(win):
    """Calculate the number of tickets required for a win."""
    return win[0] * 3 + win[1]


def solve(x1, x2, x, y1, y2, y):
    """Solve the solution to get i1 and i2.

    This function is the result of a rearranged equation for
    `x1 * i1 + x2 * i2 = x` and `y1 * i1 + y2 * i2 = y`.
    """
    i2 = (x1 * y - y1 * x) / (x1 * y2 - y1 * x2)
    if i2.is_integer():
        i1 = (x - x2 * i2) / x1
        if i1.is_integer():
            return (int(i1), int(i2))


def part_1(test: int = 0) -> int:
    """Get the solution to part 1.
    Check all the combinations to see if the output can be reached.
    """
    cheapest_wins = []
    for (x1, y1), (x2, y2), (x, y) in parse_input(test):

        max_1_presses = min((x // x1, y // y1)) + 1
        max_2_presses = min((x // x2, y // y2)) + 1

        wins = []
        for i1 in range(max_1_presses):
            for i2 in range(max_2_presses):
                if (x1 * i1 + x2 * i2) == x and (y1 * i1 + y2 * i2) == y:
                    wins.append((i1, i2))

        if wins:
            cheapest_wins.append(min(wins, key=calculate_cost))

    return sum(map(calculate_cost, cheapest_wins))


def part_2(test: int = 0) -> int:
    """Get the solution to part 1.
    This is an optimised solution using algebra rather than brute force.
    """
    cost = 0
    for (x1, y1), (x2, y2), (x, y) in parse_input(test):
        result = solve(x1, x2, x + 10000000000000, y1, y2, y + 10000000000000)
        if result:
            cost += calculate_cost(result)
    return cost


if __name__ == '__main__':
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
