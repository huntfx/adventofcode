"""Day 1: Historian Hysteria
https://adventofcode.com/2024/day/1
"""

from typing import Iterator, Tuple, List


def load_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def build_lists(test: bool = False) -> Tuple[List[int], List[int]]:
    """Build the left and right light from the text file."""
    left_list = []
    right_list = []
    for line in load_input(test):
        l, r = map(int, line.split())
        left_list.append(l)
        right_list.append(r)
    return left_list, right_list


def part_1(test: bool = False) -> int:
    """Sort the list and count the difference between each number.

    Instructions:
        Pair up the numbers and measure how far apart they are. Pair up
        the smallest number in the left list with the smallest number in
        the right list, then the second-smallest left number with the
        second-smallest right number, and so on.

        Within each pair, figure out how far apart the two numbers are;
        you'll need to add up all of those distances. For example, if
        you pair up a 3 from the left list with a 7 from the right list,
        the distance apart is 4; if you pair up a 9 with a 3, the
        distance apart is 6.

        To find the total distance between the left list and the right
        list, add up the distances between all of the pairs you found.
    """
    left_list, right_list = build_lists(test)
    return sum(abs(l - r) for l, r in zip(sorted(left_list), sorted(right_list)))


def part_2(test: bool = False) -> int:
    """Count occurances of numbers from the left list in the right list.

    Instructions:
        Figure out exactly how often each number from the left list
        appears in the right list. Calculate a total similarity score
        by adding up each number in the left list after multiplying it
        by the number of times that number appears in the right list.
    """
    left_list, right_list = build_lists(test)
    return sum(num * right_list.count(num) for num in left_list)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 11


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 31


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 1: {part_2()}')
