import math
from typing import cast
from demapples.path import find_path
from demapples.vec import Vec2


import heapq
from typing import Callable


def get_neighbours(num: int, p: Vec2) -> tuple[Vec2, ...]:
    return tuple(
        p
        for p in p.neighbours(diag=False)
        if all(a >= 0 for a in p) and is_open(num, p)
    )


def find_all_paths(
    start: Vec2,
    get_neighbours: Callable[[Vec2], tuple[Vec2, ...]],
) -> int | None:

    open_set = {start}
    open_heap = []
    g_score = {start: 0}

    heapq.heappush(open_heap, (0, start))

    while open_heap:
        g, current = heapq.heappop(open_heap)

        if current not in open_set:
            continue

        open_set.remove(current)

        if g > 50:
            return sum(g_score[x] <= 50 for x in g_score)

        for neighbor in get_neighbours(current):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (tentative_g, neighbor))
                open_set.add(neighbor)

    raise AssertionError("No path")


def is_open(num: int, p: Vec2) -> bool:
    # x*x + 3*x + 2*x*y + y + y*y
    n = p.x * p.x + 3 * p.x + 2 * p.x * p.y + p.y + p.y * p.y + num
    return n.bit_count() % 2 == 0


def solve(num: int, target: Vec2) -> int:
    result = find_path(
        Vec2(1, 1),
        target,
        lambda a, b: 1,
        lambda p: get_neighbours(num, p),
        lambda p: math.floor(p.euclidean_distance(target)),
    )
    assert result, "No solution"
    return cast(int, result[0])


def solve2(num: int) -> int:
    result = find_all_paths(Vec2(1, 1), lambda p: get_neighbours(num, p))
    assert result, "No solution"
    return result


def example(_: str) -> str:
    return str(solve(10, Vec2(7, 4)))


def star1(_: str) -> str:
    return str(solve(1358, Vec2(31, 39)))


def star2(_: str) -> str:
    result = find_all_paths(Vec2(1, 1), lambda p: get_neighbours(1358, p))
    assert result, "No solution"
    return str(result)
