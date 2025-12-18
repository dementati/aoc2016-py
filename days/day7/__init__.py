from functools import reduce


def parse(line: str) -> tuple[list[str], list[str]]:
    """
    >>> parse("jgltdnjfjsbrffzwbv[nclpjchuobdjfrpavcq]sbzanvbimpahadkk[yyoasqmddrzunoyyk]knfdltzlirrbypa")
    (['jgltdnjfjsbrffzwbv', 'sbzanvbimpahadkk', 'knfdltzlirrbypa'], ['nclpjchuobdjfrpavcq', 'yyoasqmddrzunoyyk'])
    """
    outside = []
    inside = []
    current = ""
    for c in line:
        if c == "[":
            outside.append(current)
            current = ""
        elif c == "]":
            inside.append(current)
            current = ""
        else:
            current += c

    outside.append(current)

    return outside, inside


def has_abba(seq: str) -> bool:
    """
    >>> has_abba("abba")
    True
    >>> has_abba("ioxxoj")
    True
    >>> has_abba("aaaa")
    False
    >>> has_abba("qrst")
    False
    >>> has_abba("aaaaaabba")
    True
    """

    for i in range(len(seq) - 3):
        if seq[i] == seq[i + 1]:
            continue

        if seq[i] == seq[i + 3] and seq[i + 1] == seq[i + 2]:
            return True

    return False


def get_abas(seq: str) -> set[str]:
    """
    >>> sorted(get_abas("zazbz"))
    ['zaz', 'zbz']
    """
    result = set()
    for i in range(len(seq) - 2):
        if seq[i] != seq[i + 1] and seq[i] == seq[i + 2]:
            result.add(seq[i : i + 3])

    return result


def bab(aba: str) -> str:
    assert len(aba) == 3 and aba[0] != aba[1] and aba[0] == aba[2]
    return aba[1] + aba[0] + aba[1]


def star1(input_str: str) -> str:
    result = 0
    for line in input_str.splitlines():
        outside, inside = parse(line)

        result += any(has_abba(seq) for seq in outside) and all(
            not has_abba(seq) for seq in inside
        )

    return str(result)


def star2(input_str: str) -> str:
    result = 0
    for line in input_str.splitlines():
        outside, inside = parse(line)

        outside_abas = reduce(set.union, (get_abas(seq) for seq in outside))
        inside_abas = reduce(set.union, (get_abas(seq) for seq in inside))

        result += any(bab(aba) in inside_abas for aba in outside_abas)

    return str(result)
