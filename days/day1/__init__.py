from demapples.vec import Vec2

Step = tuple[str, int]


DIRS = [
    Vec2(0, -1),
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
]


def parse_input(input_str: str) -> list[Step]:
    return [(step[0], int(step[1:])) for step in input_str.split(", ")]


def star1(input_str: str) -> str:
    """
    >>> star1("R2, L3")
    '5'
    >>> star1("R2, R2, R2")
    '2'
    >>> star1("R5, L5, R5, R3")
    '12'
    """
    curr_dir = 0
    pos = Vec2(0, 0)
    for turn, steps in parse_input(input_str):
        curr_dir = (curr_dir + (1 if turn == "R" else -1)) % 4
        pos += DIRS[curr_dir] * steps

    return str(pos.manhattan_distance(Vec2(0, 0)))


def star2(input_str: str) -> str:
    """
    >>> star2("R8, R4, R4, R8")
    '4'
    """
    curr_dir = 0
    pos = Vec2(0, 0)
    visited = set()
    for turn, steps in parse_input(input_str):
        curr_dir = (curr_dir + (1 if turn == "R" else -1)) % 4

        for _ in range(steps):
            pos += DIRS[curr_dir]

            if pos in visited:
                return str(pos.manhattan_distance(Vec2(0, 0)))

            visited.add(pos)

    raise AssertionError("No location visited twice")
