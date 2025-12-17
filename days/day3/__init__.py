from itertools import islice


def valid(sides: list[int]) -> bool:
    """
    >>> valid([5, 10, 25])
    False
    """
    mx = max(sides)
    mx_i = sides.index(mx)
    others = [s for i, s in enumerate(sides) if mx_i != i]

    return sum(others) > mx


def star1(input_str: str) -> str:
    result = 0
    for line in input_str.splitlines():
        sides = [int(s) for s in line.split()]
        result += valid(sides)

    return str(result)


def star2(input_str: str) -> str:
    arr = [line.split() for line in input_str.splitlines()]
    arr = [[int(s) for s in row] for row in zip(*arr)]

    result = 0
    for row in arr:
        for i in range(len(row) // 3):
            result += valid(row[i * 3 : i * 3 + 3])

    return str(result)
