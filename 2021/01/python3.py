from typing import List

def load_input(testing: bool = False) -> List[str]:
    """Read the input.txt file.

    Returns:
        List of each line as a string.
    """
    with open('test-input.txt'[int(not testing) * 5:], 'r') as f:
        return [line.strip('\r\n') for line in f]


def get_depths(testing: bool = False) -> List[int]:
    """Get the depths from the input file.

    Returns:
        List of depths as ints.
    """
    return list(map(int, load_input(testing=testing)))


def part_1(testing: bool = False) -> int:
    """Calculate the number of times the depth was increased."""
    depths = get_depths(testing=testing)
    return sum(1 for a, b in zip(depths, [depths[0] + 1] + depths) if a > b)


def part_2(testing: bool = False) -> int:
    """Calculate the number of times the depth was increased in groups of 3."""
    depths = get_depths(testing=testing)
    groups = [sum(depths[i: i+3]) for i in range(len(depths) - 2)]
    return sum(1 for a, b in zip(groups, [groups[0] + 1] + groups) if a > b)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(testing=True) == 7


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(testing=True) == 5


print(f'Part 1: {part_1()}')
print(f'Part 1: {part_2()}')
