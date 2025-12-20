from functools import cache
import re

from icecream import ic


def decompress(input_str: str) -> str:
    """
    >>> decompress("ADVENT")
    'ADVENT'
    >>> decompress("A(1x5)BC")
    'ABBBBBC'
    >>> decompress("(3x3)XYZ")
    'XYZXYZXYZ'
    >>> decompress("(6x1)(1x3)A")
    '(1x3)A'
    >>> decompress("X(8x2)(3x3)ABCY")
    'X(3x3)ABC(3x3)ABCY'
    """
    current = input_str
    i = 0
    while i < len(current):
        c = current[i]
        if c == "(":
            m = re.match(r"\((\d+)x(\d+)\)", current[i:])

            if m:
                a, b = (int(e) for e in m.groups())
                n = len(m.group(0))
                seq = current[i + n : i + n + a]
                rep = seq * b
                current = current[:i] + rep + current[i + n + a :]
                i = i + a * b
        else:
            i += 1

    return current


@cache
def decompress3(input_str: str) -> int:
    """
    >>> decompress3("ADVENT")
    6
    >>> decompress3("(1x12)A")
    12
    >>> decompress2("A(1x5)BC")
    7
    >>> decompress2("(3x3)XYZ")
    9
    >>> decompress2("X(8x2)(3x3)ABCY")
    20
    >>> decompress2("(27x12)(20x12)(13x14)(7x10)(1x12)A")
    241920
    """

    total = 0
    i = 0
    while i < len(input_str):
        c = input_str[i]
        if c != "(":
            i += 1
            total += 1
        else:
            m = re.match(r"\((\d+)x(\d+)\)", input_str[i:])

            if m:
                a, b = (int(e) for e in m.groups())
                n = len(m.group(0))
                seq = input_str[i + n : i + n + a]
                total += decompress3(seq) * b
                i = i + n + a

    return total


def decompress2(input_str: str) -> int:
    """
    >>> decompress2("ADVENT")
    6
    >>> decompress2("A(1x5)BC")
    7
    >>> decompress2("(3x3)XYZ")
    9
    >>> decompress2("X(8x2)(3x3)ABCY")
    20
    >>> decompress2("(27x12)(20x12)(13x14)(7x10)(1x12)A")
    241920
    """
    current = input_str
    i = 0
    total_len = 0
    while i < len(current):
        c = current[i]
        if c == "(":
            m = re.match(r"\((\d+)x(\d+)\)", current[i:])

            if m:
                a, b = (int(e) for e in m.groups())
                n = len(m.group(0))
                seq = current[i + n : i + n + a]
                rep = seq * b
                current = rep + current[i + n + a :]
                i = 0
        else:
            i += 1
            total_len += 1

    return total_len


def star1(input_str: str) -> str:
    return str(len(decompress(input_str)))


def star2(input_str: str) -> str:
    return str(decompress3(input_str))
