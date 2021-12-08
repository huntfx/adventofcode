"""Day 8: Seven Segment Search
https://adventofcode.com/2021/day/7
"""

from typing import Generator, List, Tuple


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def parse_input(test: bool = False) -> Generator[Tuple[List[str], List[str]], None, None]:
    """Convert the input to unique signal patterns and the 4 digit output value."""
    for line in load_input(test=test):
        patterns, output = [words.split() for words in line.split(' | ')]
        yield (patterns, output)


def part_1(test: bool = False):
    """Find how many unique signal patterns exist."""
    count = 0
    for patterns, output in parse_input(test=test):
        for digit in output:
            count += len(digit) in (2, 3, 4, 7)
    return count


def part_2(test: bool = False) -> int:
    """Find the sum of the outputs."""
    outputs = []
    for patterns, output in parse_input(test=test):
        known = {}
        potential_6 = []
        for pattern in map(set, patterns):
            if len(pattern) == 2:
                known[1] = pattern
            elif len(pattern) == 3:
                known[7] = pattern
            elif len(pattern) == 4:
                known[4] = pattern
            elif len(pattern) == 6:  # 0, 6, 9
                potential_6.append(pattern)
            elif len(pattern) == 7:
                known[8] = pattern

        # Initial known mapping
        a = known[7] - known[1]
        b_d = known[4] - known[1]
        e_g = known[8] - known[4] - known[7]

        for pattern in potential_6:
            # Find the mapping of e and g from 9
            if e_g - pattern:
                e = e_g - pattern
                g = e_g - e
                known[9] = known[4] | a | g

            # Find the mapping of c from 6
            elif known[7] - pattern:
                known[6] = pattern
                c = known[8] - pattern

            # Find the mapping of b and d from 0
            else:
                known[0] = pattern
                d = known[4] - known[0]
                b = b_d - d

        # Calculate the remaining mapping
        known[2] = a | c | d | e | g
        f = known[8] - known[2] - b
        known[3] = a | c | d | f | g
        known[5] = a | b | d | f | g

        # Use the mapping on the output
        digits = [next(k for k, v in known.items() if v == val) for val in map(set, output)]
        outputs.append(int(''.join(map(str, digits))))
    return sum(outputs)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 26


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 61229


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')
