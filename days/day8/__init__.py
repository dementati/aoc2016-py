from __future__ import annotations
from dataclasses import dataclass

from icecream import ic


def rotate(line: list[bool], steps: int) -> list[bool]:
    return line[-steps:] + line[:-steps]


def transpose(grid: list[list[bool]]) -> list[list[bool]]:
    return [list(row) for row in zip(*grid)]


class Grid:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.data = [[False] * w for _ in range(h)]

    def apply(self, instr: Instruction):
        match (instr.cmd):
            case "rect":
                self.rect(instr.A, instr.B)
            case "rotate row":
                self.rotate_row(instr.A, instr.B)
            case "rotate column":
                self.rotate_col(instr.A, instr.B)

    def rect(self, w: int, h: int):
        for y in range(h):
            for x in range(w):
                self.data[y][x] = True

    def rotate_row(self, row: int, steps: int):
        self.data[row] = rotate(self.data[row], steps)

    def rotate_col(self, col: int, steps: int):
        transp = transpose(self.data)
        transp[col] = rotate(transp[col], steps)
        self.data = transpose(transp)

    def __str__(self) -> str:
        result = ""
        for row in self.data:
            for b in row:
                result += "#" if b else "."
            result += "\n"
        return "\n" + result

    def __len__(self) -> int:
        return sum(sum(row) for row in self.data)


@dataclass
class Instruction:
    cmd: str
    A: int
    B: int

    @classmethod
    def from_str(cls, input_str: str) -> Instruction:
        import re

        m = re.match(
            r"(rect) (\d+)x(\d+)|(rotate row) y=(\d+) by (\d+)|(rotate column) x=(\d+) by (\d+)",
            input_str,
        )
        assert m, input_str
        ic(m.groups())
        cmd, a, b = (e for e in m.groups() if e)

        return cls(cmd, int(a), int(b))


def star1(input_str: str) -> str:
    grid = Grid(50, 6)
    for line in input_str.splitlines():
        instruction = Instruction.from_str(line)
        grid.apply(instruction)
        ic(str(grid))

    return str(len(grid))
