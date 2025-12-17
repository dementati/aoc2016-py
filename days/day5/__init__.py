import hashlib


def crack(door_id: str) -> str:
    result = ""
    i = 0
    while len(result) < 8:
        digest = hashlib.md5(f"{door_id}{i}".encode()).hexdigest()

        if digest.startswith("00000"):
            result += digest[5]

        i += 1

    return result


def crack2(door_id: str) -> str:
    result = [""] * 8
    i = 0
    seen = set()
    while len(seen) < 8:
        digest = hashlib.md5(f"{door_id}{i}".encode()).hexdigest()

        if digest.startswith("00000"):
            try:
                idx = int(digest[5])

                if 0 <= idx <= 7 and idx not in seen:
                    seen.add(idx)
                    result[idx] = digest[6]
            except ValueError:
                pass

        i += 1

    return "".join(result)


def star1(input_str: str) -> str:
    return crack(input_str)


def star2(input_str: str) -> str:
    return crack2(input_str)
