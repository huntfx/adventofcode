"""Day 9: Disk Fragmenter
https://adventofcode.com/2024/day/9
"""

from typing import Iterator


def read_input(test: bool = False) -> Iterator[str]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open(f'{"test-" if test else ""}input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def disk_map(test: bool = False) -> list[int]:
    """Load the disk map.
    Each block is represented by the file ID or -1 if empty.
    """
    output: list[int] = []
    for i, num in enumerate(next(read_input(test))):
        output.extend(-1 if i % 2 else i // 2 for _ in range(int(num)))
    return output


def part_1(test: bool = False) -> int:
    """Rearrange the data one block at a time."""
    data = disk_map(test)
    total_space = len(data)

    while True:
        # Trim any free space from the end
        while data[-1] < 0:
            del data[-1]
            total_space -= 1

        # Work backwards
        for i in range(total_space, 0, -1):
            # Skip if the data isn't empty
            if data[i - 1] < 0:
                continue

            # Find the next free space block
            try:
                j = data.index(-1)
            except ValueError:
                return sum(i * j for i, j in enumerate(data))

            # Swap the data
            data[j], data[i - 1] = data[i - 1], data[j]
            break


def part_2(test: bool = False) -> int:
    """Rearrange the data keeping file blocks together."""
    data = disk_map(test)

    for current_id in range(max(data), 0, -1):

        # Find the current file block
        file_index = data.index(current_id)
        block_size = data.count(current_id)
        block_data = data[file_index:file_index + block_size]
        empty_block = [-1] * block_size

        # Search for the next empty block
        for i in range(data.index(-1), file_index):
            if data[i:i + block_size] == empty_block:
                data[i:i + block_size], data[file_index:file_index + block_size] = block_data, empty_block
                break

    return sum(i * j for i, j in enumerate(data) if j > 0)


def test_part_1() -> None:
    """Check part 1 against the test input."""
    assert part_1(test=True) == 1928


def test_part_2() -> None:
    """Check part 2 against the test input."""
    assert part_2(test=True) == 2858


if __name__ == '__main__':
    test_part_1()
    print(f'Part 1: {part_1()}')
    test_part_2()
    print(f'Part 2: {part_2()}')

