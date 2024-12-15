from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import numpy as np
from scipy.ndimage import label


BASE = Path(__file__).parent.parent

TESTS_DIR = BASE / 'test-data'

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

DIRECTIONS_STRUCTURE = np.array([[0, 1, 0],
                                 [1, 1, 1],
                                 [0, 1, 0]])


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


def index_valid(data: np.ndarray, index: tuple[int, int]) -> bool:
    """Determine if an index is valid for a given 2D array."""
    return 0 <= index[0] < data.shape[0] and 0 <= index[1] < data.shape[1]


def load_garden(test: int = 0) -> np.ndarray:
    """Load the input into a 2D array for the map."""
    return np.array([list(line) for line in read_input(test)])


def calculate_plant_cost(garden: np.ndarray, plant: str) -> int:
    """Calculate the cost of a plant in a garden.

    The cost is the product of the area of the plant and its total
    perimeter. More than one plot may exist at once in a garden.
    """
    plant_groups, num_groups = label(garden == plant, structure=DIRECTIONS_STRUCTURE)  # type: ignore
    if TYPE_CHECKING:
        assert isinstance(plant_groups, np.ndarray)
        assert isinstance(num_groups, int)

    cost = 0
    for group in range(1, num_groups + 1):
        plant_group = plant_groups == group

        # The area is just the size of the group
        area = np.sum(plant_group)

        # Calculate the perimeter by removing one for each neighbour
        perimeter = area * 4
        for current in zip(*np.where(plant_group)):
            for direction in DIRECTIONS:
                neighbour = (current[0] + direction[0], current[1] + direction[1])
                if index_valid(plant_group, neighbour) and plant_group[neighbour]:
                    perimeter -= 1

        cost += area * perimeter

    return cost


def part_1(test: int = 0) -> int:
    """Get the solution to part 1."""
    garden = load_garden(test)
    return sum(calculate_plant_cost(garden, plant) for plant in np.unique(garden))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    run_tests()
    print(f'Part 1: {part_1()}')
