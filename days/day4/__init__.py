from itertools import groupby
import re
from typing import Counter


Entry = tuple[str, int, str]


def parse(entry: str) -> Entry:
    """
    >>> parse("aaaaa-bbb-z-y-x-123[abxyz]")
    ('aaaaa-bbb-z-y-x', 123, 'abxyz')
    >>> parse("totally-real-room-200[decoy]")
    ('totally-real-room', 200, 'decoy')
    """
    m = re.match(r"([\w-]+)-(\d+)\[(\w+)\]", entry)
    assert m
    name = m.group(1)
    sector = int(m.group(2))
    checksum = m.group(3)
    return name, sector, checksum


def valid(entry: Entry) -> bool:
    """
    >>> valid(parse("aaaaa-bbb-z-y-x-123[abxyz]"))
    True
    >>> valid(parse("a-b-c-d-e-f-g-h-987[abcde]"))
    True
    >>> valid(parse("not-a-real-room-404[oarel]"))
    True
    >>> valid(parse("totally-real-room-200[decoy]"))
    False
    """
    name, _, checksum = entry

    name = name.replace("-", "")

    sorted_items = sorted(Counter(name).items(), key=lambda i: -i[1])

    computed_checksum = ""
    for _, g in groupby(sorted_items, key=lambda i: i[1]):
        computed_checksum += "".join(sorted(k for k, _ in g))

    computed_checksum = computed_checksum[:5]

    return checksum == computed_checksum


def decrypt(name: str, sector: int) -> str:
    """
    >>> decrypt("qzmt-zixmtkozy-ivhz", 343)
    'very-encrypted-name'
    """

    def idx(c: str) -> int:
        return ord(c) - ord("a")

    def ch(i: int) -> str:
        return chr(i + ord("a"))

    result = ""
    for c in name:
        result += c if c == "-" else ch((idx(c) + sector) % 26)

    return result


def star1(input_str: str) -> str:
    result = 0
    for line in input_str.splitlines():
        entry = parse(line)
        if valid(entry):
            _, sector, _ = entry
            result += sector

    return str(result)


def star2(input_str: str) -> str:
    result = "\n"
    for line in input_str.splitlines():
        entry = parse(line)
        if valid(entry):
            name, sector, _ = entry
            result += f"{sector}: {decrypt(name, sector)}\n"

    return result
