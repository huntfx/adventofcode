"""Day 4: Giant Squid
https://adventofcode.com/2021/day/4
"""

import numpy as np
from typing import Generator, List, Optional


def load_input(test: bool = False) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('test-input.txt'[int(not test) * 5:], 'r') as f:
        for line in f:
            yield line.strip('\r\n')


class BingoBoard(object):
    """Store the state of the bingo board."""

    def __init__(self, cells: List[List[int]]) -> None:
        """Initialise the board from a list.
        Assumes the cells are in a 5x5 grid.
        """
        self._cells = np.array(cells, dtype=int)
        self._won = np.full(self._cells.shape, False, dtype=bool)
        self._last_move = None

    def __repr__(self) -> str:
        """Show the board state."""
        return self._cells.__repr__()

    def won(self) -> bool:
        """Determine if the game has been won."""
        for x in range(5):
            if np.all(self._won[x,:]):
                return True
        for y in range(5):
            if np.all(self._won[:,y]):
                return True
        return False

    def play(self, num) -> bool:
        """Play a number.
        Returns if the game was won.
        """
        self._last_move = num
        where = np.where(self._cells == num)
        self._won[where] = True
        return self.won()

    def score(self) -> int:
        """Get the board score."""
        where = np.where(self._won == False)
        unmarked = np.sum(self._cells[where])
        return unmarked * self._last_move


def get_choices(test: bool = False) -> Generator[int, None, None]:
    """Iterate through all the choices."""
    raw = next(load_input(test=test))
    for choice in raw.split(','):
        yield int(choice)


def get_boards(test: bool = False) -> Generator[BingoBoard, None, None]:
    """Iterate through all the boards."""
    cells: List[List[int]] = []
    for line in list(load_input(test=test))[2:]:
        if line:
            cells.append([])
            for c in line.split():
                cells[-1].append(int(c))
        elif cells:
            yield BingoBoard(cells)
            cells = []
    if cells:
        yield BingoBoard(cells)


def part_1(test: bool = False) -> Optional[int]:
    """Find the winning board."""
    boards = list(get_boards(test=test))
    for choice in get_choices(test=test):
        for board in boards:
            if board.play(choice):
                return board.score()
    return None


def part_2(test: bool = False) -> Optional[int]:
    """Find the losing board."""
    boards = list(get_boards(test=test))
    for choice in get_choices(test=test):
        for board in frozenset(boards):
            if board.play(choice):
                boards.remove(board)
                if not boards:
                    return board.score()
    return None


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 4512


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 1924


if __name__ == '__main__':
    print(f'Part 1: {part_1()}')
    print(f'Part 2: {part_2()}')
