from __future__ import annotations
import itertools
import re
from typing import cast

from demapples.path import find_path


FLOORS = {
    "first": 0,
    "second": 1,
    "third": 2,
}


def set2(x: int, value: int, offset: int) -> int:
    assert 0 <= value < 4
    mask = 0b11 << offset
    return (x & ~mask) | (value << offset)


def get2(x: int, offset: int) -> int:
    return (x >> offset) & 0b11


class State:
    def __init__(self, count: int, bitmap: int = 0):
        self.count = count
        self.bitmap = bitmap

    def __hash__(self) -> int:
        return self.bitmap

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.bitmap == other.bitmap

    def __lt__(self, other: State) -> bool:
        return self.bitmap < other.bitmap

    @classmethod
    def from_pairs(
        cls, count: int, elevator_floor: int, pairs: list[tuple[int, int]]
    ) -> State:
        bitmap = 0
        offset = 0
        bitmap = set2(bitmap, elevator_floor, 0)

        for m, g in pairs:
            offset += 2
            bitmap = set2(bitmap, m, offset)
            offset += 2
            bitmap = set2(bitmap, g, offset)

        return State(count, bitmap)

    def pairs(self) -> list[tuple[int, int]]:
        """
        >>> pairs = [(0, 1), (2, 3), (2, 1)]
        >>> state = State.from_pairs(["A", "B", "C"], 1, pairs)
        >>> state.to_pairs() == pairs
        True
        """
        result = []
        for i in range(self.count):
            offset = 2 + i * 4
            result.append((get2(self.bitmap, offset), get2(self.bitmap, offset + 2)))

        return result

    def elevator(self) -> int:
        return get2(self.bitmap, 0)

    def valid(self) -> bool:
        pairs = self.pairs()
        gen_floors = {g for _, g in pairs}
        return all((m == g) or (m not in gen_floors) for m, g in pairs)

    def transitions(self) -> set[State]:
        pairs = self.pairs()

        # 1. Iterate over adjacent elevator positions
        elevator_floor = self.elevator()

        result = set()
        for d in (-1, 1):
            if elevator_floor + d < 0 or elevator_floor + d > 3:
                continue

            # 1.1. Get all objects on floor
            movables = []
            for i, (m, g) in enumerate(pairs):
                if m == elevator_floor:
                    movables.append((i, False))
                if g == elevator_floor:
                    movables.append((i, True))

            # 1.2. Iterate over all 1,2 combinations of floor_objects
            for k in (1, 2):
                for combo in itertools.combinations(movables, k):
                    # If move is valid, add to results
                    state = self
                    new_pairs = [list(p) for p in pairs]
                    for i, is_gen in combo:
                        new_pairs[i][is_gen] += d

                    new_pairs = sorted([(m, g) for m, g in new_pairs])

                    state = State.from_pairs(
                        self.count,
                        elevator_floor + d,
                        new_pairs,
                    )

                    if state.valid():
                        result.add(state)

        return result

    def __str__(self) -> str:
        pairs = self.pairs()

        result = "\n"
        for floor in range(3, -1, -1):
            result += f"F{floor + 1} "

            if floor == self.elevator():
                result += "e  "
            else:
                result += ".  "

            for idx, (chip, gen) in enumerate(pairs):
                if floor == chip:
                    result += chr(97 + idx) + "m "
                else:
                    result += ".  "

                if floor == gen:
                    result += chr(97 + idx) + "g "
                else:
                    result += ".  "

            result += "\n"

        return result.upper()

    def end(self) -> State:
        return State.from_pairs(self.count, 3, [(3, 3)] * self.count)

    @classmethod
    def initial(
        cls,
        microchips: list[tuple[int, int]],
        generators: list[tuple[int, int]],
    ) -> State:
        """
        >>> state = State.initial(["A"], [(0, 0)], [(1, 0)])
        >>> state.get_elevator_floor()
        0
        """
        assert len(microchips) == len(generators)

        pairs = {}

        for floor, mic_idx in microchips:
            pairs[mic_idx] = [floor]

        for floor, gen_idx in generators:
            pairs[gen_idx].append(floor)

        return State.from_pairs(len(microchips), 0, sorted(pairs.values()))

    @classmethod
    def from_str(cls, input_str: str) -> State:
        elements = []
        microchips = []
        generators = []

        def parse_object(rest: str):
            m = re.match(r"(\w+)-compatible microchip", rest)
            if m:
                element = m.group(1)
                if element not in elements:
                    elements.append(element)

                microchips.append((floor, elements.index(element)))
            else:
                m = re.match(r"(\w+) generator", rest)

                if m:
                    element = m.group(1)
                    if element not in elements:
                        elements.append(element)

                    generators.append((floor, elements.index(element)))
                else:
                    raise AssertionError("Couldn't parse object from: " + rest)

        for line in input_str.splitlines():
            m = re.match(r"^The (\w+) floor contains a ", line)
            if not m:
                continue

            floor = FLOORS[m.group(1)]
            rest = line.removeprefix(m.group(0))
            obj_strs = re.split(r" and a |, a |, and a ", rest)
            for obj_str in obj_strs:
                parse_object(obj_str)

        return cls.initial(microchips, generators)

    def heuristic(self) -> int:
        return sum(6 - m - g for m, g in self.pairs()) // 2


def solve(initial: State) -> int:
    result = find_path(
        initial,
        initial.end(),
        lambda a, b: 1,
        lambda s: tuple(s.transitions()),
        lambda s: s.heuristic(),
    )

    assert result
    return cast(int, result[0])


def star1(input_str: str) -> str:
    return str(solve(State.from_str(input_str)))


def star2(input_str: str) -> str:
    state = State.from_str(input_str)
    state = State.from_pairs(state.count + 2, 0, state.pairs() + [(0, 0), (0, 0)])
    return str(solve(state))
