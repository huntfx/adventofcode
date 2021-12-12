"""Day 12: Passage Pathing
https://adventofcode.com/2021/day/12
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union
from string import ascii_lowercase


def load_input(test_case: int = 0) -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    path = f'test-input{test_case}.txt' if test_case else 'input.txt'
    with open(path, 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def build_connections(test_case: int = 0) -> Dict[Cave, List[Cave]]:
    """Build the connections dictionary."""
    connections = defaultdict(list)
    for line in load_input(test_case=test_case):
        start, end = (Cave(code, test_case) for code in line.split('-'))
        connections[start].append(end)
        connections[end].append(start)
    return connections


class Cave(object):
    """Store the cave object and any related connections."""

    __slots__ = ('code', 'test_case')
    _Connections: Dict[int, Dict[Cave, List[Cave]]] = {}

    def __init__(self, code: Union[str, Cave], test_case: int = 0):
        """Initialise the cave.

        Parameters:
            code: Name of the cave.
            test_case: Load the connections for a particular test.
        """
        if isinstance(code, Cave):
            code = code.code

        self.code: str = code
        self.test_case: int = test_case

    @classmethod
    def _connections(cls, test_case: int = 0) -> Dict[Cave, List[Cave]]:
        """Cache and get the connections for a current test case."""
        if test_case not in cls._Connections:
            cls._Connections[test_case] = build_connections(test_case=test_case)
        return cls._Connections[test_case]

    @classmethod
    def all(cls, test_case: int = 0) -> List[Cave]:
        """Get all the caves."""
        return list(cls._connections(test_case).keys())

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.code}, test_case={self.test_case})'

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cave):
            return self.code == other.code and self.test_case == other.test_case
        return self.code == other

    def is_start(self) -> bool:
        """Determine if this is the start cave."""
        return self.code == 'start'

    def is_end(self) -> bool:
        """Determine if this is the end cave."""
        return self.code == 'end'

    def is_small(self) -> bool:
        """Determine if this is a small cave."""
        if self.is_start() or self.is_end():
            return False
        return all(c in ascii_lowercase for c in self.code)

    def is_large(self) -> bool:
        """Determine if this is a large cave."""
        return not self.is_small()

    def connections(self) -> List[Cave]:
        """Get the direct connections to this cave."""
        return self._connections(self.test_case)[self]

    def find_paths(self, target: Union[Cave, str],
                   visit_twice: Optional[Union[Cave, str]] = None) -> List[List[Cave]]:
        """Find paths to the target."""
        target = Cave(target, self.test_case)
        return find_paths(node=self, target=target, visit_twice=visit_twice)


def find_paths(node: Cave, target: Union[Cave, str], visit_twice: Optional[Union[Cave, str]] = None,
               _path: Optional[List[Cave]] = None, _visited: Optional[Set[Cave]] = None) -> List[List[Cave]]:
    """Recursively walk through the connections to find paths to the target.

    Parameters:
        node: Node to check the connections for.
        target: Node to try and reach.
        visit_twice: Allow a small cave to be visited twice.

    Returns:
        List of cave paths, where each path is a list of caves.
    """
    if _path is None:
        _path = []
    if _visited is None:
        _visited = {node}
    else:
        _visited = set(_visited)

    # Handle visit limits
    if node.is_small():
        if node == visit_twice:
            visit_twice = None
        else:
            _visited.add(node)

    paths = []
    for connection in node.connections():
        # Found the target
        if connection == target:
            paths.append(_path)

        # Recursively search further
        elif connection not in _visited:
            result = find_paths(connection, target, visit_twice=visit_twice,
                                _path=_path + [connection], _visited=_visited)
            paths.extend(result)
    return paths


def part_1(test_case: int = 0) -> int:
    """Find the number of paths to the end."""
    return len(Cave('start', test_case).find_paths('end'))


def part_2(test_case: int = 0) -> int:
    """Find the number of paths to end, with visiting a single small cave twice."""
    paths = []
    for cave in Cave.all(test_case):
        if cave.is_small():
            paths.extend(Cave('start', test_case).find_paths('end', visit_twice=cave))
    return len(set(map(tuple, paths)))


def test_part_1_1() -> None:
    """Check part 1 against the test case 1 input."""
    assert part_1(test_case=1) == 10


def test_part_1_2() -> None:
    """Check part 1 against the test case 2 input."""
    assert part_1(test_case=2) == 19


def test_part_1_3() -> None:
    """Check part 1 against the test case 3 input."""
    assert part_1(test_case=3) == 226


def test_part_2_1() -> None:
    """Check part 2 against the test case 1 input."""
    assert part_2(test_case=1) == 36


def test_part_2_2() -> None:
    """Check part 2 against the test case 2 input."""
    assert part_2(test_case=2) == 103


def test_part_2_3() -> None:
    """Check part 2 against the test case 3 input."""
    assert part_2(test_case=3) == 3509


if __name__ == '__main__':
    test_part_1_1()
    test_part_1_2()
    test_part_1_3()
    print(f'Part 1: {part_1()}')
    test_part_2_1()
    test_part_2_2()
    test_part_2_3()
    print(f'Part 2: {part_2()}')
