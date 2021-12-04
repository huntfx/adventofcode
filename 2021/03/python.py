"""Day 3: Binary Diagnostic
https://adventofcode.com/2021/day/3
"""

import operator
from collections import Counter
from typing import Callable, List


def load_input(test: bool = False) -> List[str]:
    """Read the input.txt file.

    Returns:
        List of each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        return [line.strip('\r\n') for line in f]


class BinaryList(object):
    """Class to store the list of binary numbers."""

    def __init__(self, test: bool = False) -> None:
        """Initialise the class with the raw input."""
        self.raw = load_input(test=test)

    def __len__(self) -> int:
        """Get the length of the binary numbers."""
        return self.raw[0].__len__()

    def _calculate_rate(self, op: Callable) -> int:
        """Calculate the gamma or epsilon rate."""
        counts = (Counter(item[i] for item in self.raw) for i in range(self.__len__()))
        binary = (op(count['0'], count['1']) for count in counts)
        return int(''.join(map(str, map(int, binary))), 2)

    def gamma(self) -> int:
        """Get the gamma rate."""
        return self._calculate_rate(operator.lt)

    def epsilon(self) -> int:
        """Get the epsilon rate."""
        return self._calculate_rate(operator.gt)

    def power_consumption(self) -> int:
        """Calculate the power consumption."""
        return self.gamma() * self.epsilon()

    def _calculate_rating(self, use_most_common: bool = True) -> int:
        """Calculate the oxygen or co2 rating."""
        bits = '01' if use_most_common else '10'

        current = self.raw
        for i in range(self.__len__()):
            counter = Counter(item[i] for item in current)
            current = [binary_num for binary_num in current
                       if binary_num[i] == bits[1] and (counter['1'] >= counter['0'])
                       or binary_num[i] == bits[0] and counter['0'] > counter['1']]
            if not current:
                break
            result = current
        return int(result[0], 2)

    def oxygen(self) -> int:
        """Get the oxygen rating."""
        return self._calculate_rating(use_most_common=True)

    def co2(self) -> int:
        """Get the CO2 rating."""
        return self._calculate_rating(use_most_common=False)

    def life_support_rating(self) -> int:
        """Calculate the life support rating."""
        return self.oxygen() * self.co2()


def part_1(test: bool = False) -> int:
    """Get the power consumption."""
    return BinaryList(test=test).power_consumption()


def part_2(test: bool = False) -> int:
    """Get the life support rating."""
    return BinaryList(test=test).life_support_rating()


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 198


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 230


if __name__ == '__main__':
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
