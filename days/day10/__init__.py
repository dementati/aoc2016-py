from __future__ import annotations
from collections import defaultdict
import math
import re


def solve(input_str: str, part2: bool = False) -> str:
    bins = defaultdict(list)
    rules = {}

    for line in input_str.splitlines():
        m = re.match(r"value (\d+) goes to (bot \d+)", line)

        if m:
            value, bot = m.groups()
            bins[bot].append(int(value))
        else:
            m = re.match(
                r"(bot \d+) gives low to (\w+ \d+) and high to (\w+ \d+)",
                line,
            )

            if m:
                bot, low, high = m.groups()
                rules[bot] = (low, high)
            else:
                raise AssertionError(f"Invalid input: {line}")

    part1 = None
    while any(len(bins[bot]) > 0 for bot in bins if bot.startswith("bot")):
        for bot, (low, high) in rules.items():
            assert len(bins[bot]) < 3, f"{bot}: {bins[bot]}"

            if len(bins[bot]) != 2:
                continue

            if not part2 and set(bins[bot]) == {61, 17}:
                return bot

            low_v = min(bins[bot])
            high_v = max(bins[bot])
            bins[bot] = []
            bins[low].append(low_v)
            bins[high].append(high_v)

    return str(math.prod(bins[f"output {i}"][0] for i in range(3)))


def star1(input_str: str) -> str:
    return solve(input_str)


def star2(input_str: str) -> str:
    return solve(input_str, part2=True)
