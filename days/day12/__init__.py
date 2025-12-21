from collections import defaultdict


REGISTERS = "abcd"


def solve(input_str: str, init_c: int = 0) -> int:
    program = input_str.splitlines()
    ip = 0
    reg = defaultdict(int)

    reg["c"] = init_c

    while ip < len(program):
        cmd, *args = program[ip].split()

        assert "1" not in reg

        match cmd:
            case "cpy":
                value = reg[args[0]] if args[0] in REGISTERS else int(args[0])
                reg[args[1]] = value
            case "inc":
                reg[args[0]] += 1
            case "dec":
                reg[args[0]] -= 1
            case "jnz":
                value = reg[args[0]] if args[0] in REGISTERS else int(args[0])
                if value != 0:
                    ip += int(args[1])
                    continue

        ip += 1

    return reg["a"]


def star1(input_str: str) -> str:
    return str(solve(input_str))


def star2(input_str: str) -> str:
    return str(solve(input_str, init_c=1))
