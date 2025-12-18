from typing import Counter


def star1(input_str: str) -> str:
    result = ""
    for col in zip(*input_str.splitlines()):
        k, _ = max(Counter(col).items(), key=lambda t: t[1])
        result += k

    return result


def star2(input_str: str) -> str:
    result = ""
    for col in zip(*input_str.splitlines()):
        k, _ = min(Counter(col).items(), key=lambda t: t[1])
        result += k

    return result
