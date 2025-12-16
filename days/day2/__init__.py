from demapples.vec import Vec2

DELTA = {
    "U": Vec2(0, -1),
    "L": Vec2(-1, 0),
    "R": Vec2(1, 0),
    "D": Vec2(0, 1),
}

KEYMAP = ("  1  \n" " 234 \n" "56789\n" " ABC \n" "  D  ").splitlines()


def read_line(pos: Vec2, line: str) -> Vec2:
    for c in line:
        pos += DELTA[c]
        pos = pos.bounded(Vec2(2, 2))

    return pos


def read_line2(pos: Vec2, line: str) -> Vec2:
    for c in line:
        new_pos = pos + DELTA[c]
        if new_pos.manhattan_distance(Vec2(2, 2)) <= 2:
            pos = new_pos

    return pos


def key(pos: Vec2) -> str:
    """
    >>> key(Vec2(0, 0))
    '1'
    >>> key(Vec2(1, 0))
    '2'
    >>> key(Vec2(2, 0))
    '3'
    >>> key(Vec2(0, 1))
    '4'
    """
    return str(1 + pos.y * 3 + pos.x)


def key2(pos: Vec2) -> str:
    return KEYMAP[pos.y][pos.x]


def star1(input_str: str) -> str:
    result = ""
    pos = Vec2(1, 1)
    for line in input_str.splitlines():
        pos = read_line(pos, line)
        result += key(pos)

    return result


def star2(input_str: str) -> str:
    result = ""
    pos = Vec2(0, 2)
    for line in input_str.splitlines():
        pos = read_line2(pos, line)
        result += key2(pos)

    return result
