"""Day 16: Packet Decoder
https://adventofcode.com/2021/day/16
"""

from __future__ import annotations

import math
from typing import Callable, Dict, Generator, List, Optional, Tuple


def load_input() -> Generator[str, None, None]:
    """Read the input.txt file.

    Yields:
        Each line as a string.
    """
    with open('input.txt', 'r') as f:
        for line in f:
            yield line.strip('\r\n')


def load_hex() -> str:
    """Load the input and return the hex string."""
    return next(load_input())


def gt(args: Generator[int, None, None]) -> bool:
    """Determine if the first value is greater than the second."""
    return next(args) > next(args)


def lt(args: Generator[int, None, None]) -> bool:
    """Determine if the first value is less than the second."""
    return next(args) < next(args)


def eq(args: Generator[int, None, None]) -> bool:
    """Determine if 2 values are equal."""
    return next(args) == next(args)


class Packet(object):
    """Store a heirarchy of packets."""

    __slots__ = ('type', 'version', 'value', 'subpackets')

    # Map the functions to the packet types
    FUNCTION_MAP: List[Callable] = [sum, math.prod, min, max, lambda args: 0, gt, lt, eq]

    # Give nicer names to some of the functions
    FNAME_OVERRIDE: Dict[str, str] = {'prod': 'math.prod', 'gt': 'operator.gt',
                                      'lt': 'operator.lt', 'eq': 'operator.eq'}

    def __init__(self, version: int, type: int) -> None:
        """Set up the base packet."""
        self.type: int = type
        self.version: int = version
        self.value: int = 0
        self.subpackets: List[Packet] = []

    def __repr__(self) -> str:
        """Display the full formula in valid Python code."""
        if self.type == 4:
            return str(self.value)
        fname = self.FUNCTION_MAP[self.type].__name__
        lines = [f'{self.FNAME_OVERRIDE.get(fname, fname)}(']
        for packet in self.subpackets:
            lines.append('\n'.join('  ' + line for line in repr(packet).split('\n')) + ',')
        lines.append(')')
        return '\n'.join(lines)

    def __iter__(self) -> Generator[Packet, None, None]:
        """Iterate through every packet, including the current one."""
        yield self
        for packet in self.subpackets:
            yield from packet

    def eval(self) -> int:
        """Evaluate the stack of packets."""
        return self.FUNCTION_MAP[self.type](packet.eval() for packet in self.subpackets) + self.value


def hex_to_bin(hex: str) -> str:
    """Convert hex characters to a binary format.
    This converts each character separately.
    """
    return ''.join(bin(int(str(c), 16))[2:].zfill(4) for c in str(hex))


def _build_packet(binary: str) -> Tuple[Packet, int]:
    """Create a packet from the binary string.
    It may contain sub packets.

    Returns:
        Packet and length of binary used to generate it.
    """
    version = int(binary[:3], 2)
    packet_type = int(binary[3:6], 2)
    packet = Packet(version, packet_type)

    # Literal value
    if packet_type == 4:

        # Split groups into chunks of 5, ignoring trailing data
        data = binary[6:]
        groups = [data[i * 5:(i+1) * 5] for i in range(len(data) // 5)]

        # Iterate through groups until the first character is 0
        result = []
        while groups[0].startswith('1'):
            result.append(groups.pop(0)[1:])
        result.append(groups.pop(0)[1:])

        value = int(''.join(result), 2)
        packet.value = value
        return packet, 6 + 5 * len(result)

    # Contains multiple values
    else:
        length_type_id = binary[6]

        # Contains length of subpackets
        if length_type_id == '0':
            subpacket_length = int(binary[7:22], 2)

            data = binary[22:22 + subpacket_length]
            while data:
                subpacket, offset = _build_packet(data)
                packet.subpackets.append(subpacket)
                data = data[offset:]
            length = subpacket_length + 22

        # Contains count of subpackets
        elif length_type_id == '1':
            subpacket_count = int(binary[7:18], 2)

            length = 18
            data = binary[18:]
            for _ in range(subpacket_count):
                subpacket, offset = _build_packet(data)
                packet.subpackets.append(subpacket)
                data = data[offset:]
                length += offset

        return packet, length


def build_packet(binary: str) -> Packet:
    """Build a packet from a binary string."""
    return _build_packet(binary=binary)[0]


def part_1(hex: Optional[str] = None) -> int:
    """Find the sum of contained versions."""
    if hex is None:
        hex = load_hex()
    packet = build_packet(hex_to_bin(hex))
    return sum(subpacket.version for subpacket in packet)


def part_2(hex: Optional[str] = None) -> int:
    """Find the result of the packet calculation."""
    if hex is None:
        hex = load_hex()
    packet = build_packet(hex_to_bin(hex))
    return packet.eval()


def test_part_1_1() -> None:
    """Check part 1 against test input 1."""
    assert part_1('8A004A801A8002F478') == 16


def test_part_1_2() -> None:
    """Check part 1 against test input 2."""
    assert part_1('620080001611562C8802118E34') == 12


def test_part_1_3() -> None:
    """Check part 1 against test input 3."""
    assert part_1('C0015000016115A2E0802F182340') == 23


def test_part_1_4() -> None:
    """Check part 1 against test input 4."""
    assert part_1('A0016C880162017C3686B18A3D4780') == 31


def test_part_2_1() -> None:
    """Check part 2 against test input 1."""
    assert part_2('C200B40A82') == 3


def test_part_2_2() -> None:
    """Check part 2 against test input 2."""
    assert part_2('04005AC33890') == 54


def test_part_2_3() -> None:
    """Check part 2 against test input 3."""
    assert part_2('880086C3E88112') == 7


def test_part_2_4() -> None:
    """Check part 2 against test input 4."""
    assert part_2('CE00C43D881120') == 9


def test_part_2_5() -> None:
    """Check part 2 against test input 5."""
    assert part_2('D8005AC2A8F0') == 1


def test_part_2_6() -> None:
    """Check part 2 against test input 6."""
    assert part_2('F600BC2D8F') == 0


def test_part_2_7() -> None:
    """Check part 2 against test input 7."""
    assert part_2('9C005AC2F8F0') == 0


def test_part_2_8() -> None:
    """Check part 2 against test input 8."""
    assert part_2('9C0141080250320F1802104A08') == 1


if __name__ == '__main__':
    test_part_1_1()
    test_part_1_2()
    test_part_1_3()
    test_part_1_4()
    print(f'Part 1: {part_1()}')
    test_part_2_1()
    test_part_2_2()
    test_part_2_3()
    test_part_2_4()
    test_part_2_5()
    test_part_2_6()
    test_part_2_7()
    test_part_2_8()
    print(f'Part 2: {part_2()}')
