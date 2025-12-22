from collections import Counter
import hashlib
from itertools import count
import re
from typing import Callable


def get_digest(salt: str, idx: int) -> str:
    return hashlib.md5(f"{salt}{idx}".encode()).hexdigest()


def get_stretched_digest(salt: str, idx: int) -> str:
    result = f"{salt}{idx}"
    for _ in range(2017):
        result = hashlib.md5(result.encode()).hexdigest()

    return result


def generate_keys(salt: str, digest_func: Callable[[str, int], str]) -> int:
    candidates = {}
    matches = Counter()

    keys = []

    for idx in count(0):
        digest = digest_func(salt, idx)

        to_delete = []
        for pidx in candidates:
            if idx - pidx > 1000:
                to_delete.append(pidx)

        for pidx in to_delete:
            if matches[pidx] == 1:
                keys.append(candidates[pidx][1])

                if len(keys) == 64:
                    return pidx

            del candidates[pidx]
            del matches[pidx]

        for pidx, (c, _) in candidates.items():
            m = re.search(c + r"{5}", digest)
            if m:
                matches[pidx] += 1

        m = re.search(r"([a-z0-9])\1{2}", digest)
        if m:
            candidates[idx] = (m.group(1), digest)

    raise AssertionError("Unreachable")


def star1(input_str: str) -> str:
    return str(generate_keys(input_str, get_digest))


def star2(input_str: str) -> str:
    return str(generate_keys(input_str, get_stretched_digest))
