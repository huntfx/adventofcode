from collections import defaultdict
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

        for fn in (part_1, part_2):
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


def iter_plant_details(garden: np.ndarray, plant: str) -> Iterator[tuple[int, int, int]]:
    """Get the details of a plant in the garden.
    This will yield values per region of the requested plant.

    Yields:
        Area, perimeter, sides.
    """
    plant_groups, num_groups = label(garden == plant, structure=DIRECTIONS_STRUCTURE)  # type: ignore
    if TYPE_CHECKING:
        assert isinstance(plant_groups, np.ndarray)
        assert isinstance(num_groups, int)

    # Iterate over each region of this particular plant type
    for plant_region in map(plant_groups.__eq__, range(1, num_groups + 1)):
        area = 0
        perimeter = 0
        sides = 0

        # Get the area
        area += np.sum(plant_region)

        # Get the perimeter and all the edges
        edge_groups = [defaultdict(set) for _ in range(2)]
        for current in zip(*np.where(plant_region)):
            for direction in DIRECTIONS:
                neighbour = (current[0] + direction[0], current[1] + direction[1])

                # Skip if within the same region
                if index_valid(plant_region, neighbour) and plant_region[neighbour]:
                    continue

                # An edge was detected so add to the perimeter
                perimeter += 1

                # Record edge in groups of horizontal / vertical
                for i, edges in enumerate(edge_groups):
                    if current[i] == neighbour[i]:
                        edges[current[i]].add((current[not i], neighbour[not i]))

        # Calculate which edges are contiguous
        for edge_group in edge_groups:
            current_pairs: set[tuple[int, int]] = set()
            for _, side_pairs in sorted(edge_group.items()):
                current_pairs &= side_pairs
                sides += len(side_pairs - current_pairs)
                current_pairs |= side_pairs

        yield area, perimeter, sides


def calculate_plant_cost(garden: np.ndarray, plant: str, discount: bool) -> int:
    """Calculate the cost of a plant in a garden.

    The cost is the product of the area of the plant and its total
    perimeter. More than one plot may exist at once in a garden.
    """
    cost = 0
    for area, perimeter, sides in iter_plant_details(garden, plant):
        if discount:
            cost += area * sides
        else:
            cost += area * perimeter
    return cost


def part_1(test: int = 0) -> int:
    """Get the solution to part 1."""
    garden = load_garden(test)
    return sum(calculate_plant_cost(garden, plant, False) for plant in np.unique(garden))


def part_2(test: int = 0) -> int:
    """Get the solution to part 2."""
    garden = load_garden(test)
    return sum(calculate_plant_cost(garden, plant, True) for plant in np.unique(garden))


if __name__ == '__main__':
    run_tests()
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')

