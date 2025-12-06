import math
from typing import List

Data = List[List[str]]

EXAMPLE = "\n".join(
    [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  ",
    ]
)
OPERATORS = {"*": math.prod, "+": sum}


def step1(data: str) -> int:
    rows = [row.split() for row in data.splitlines() if row.strip()]
    cols = zip(*rows)  # transpose to columns
    total = 0
    for col in cols:
        numbers = [int(num) for num in col[:-1]]
        total += OPERATORS[col[-1]](numbers)
    return total


def step2(data: Data) -> int:
    work_queue = []
    total = 0
    for col in data:
        if number_str := "".join(col[:-1]).strip():
            work_queue.append(int(number_str))
        if col[-1] in OPERATORS:
            total += OPERATORS[col[-1]](work_queue)
            work_queue.clear()
    return total


# Could probably refactor to share parsing with step1, but meeh..
def parse_2d_array(data: str) -> Data:
    lines = [line for line in data.splitlines() if line.strip()]
    cols = list(zip(*lines))  # Problem seems col centric, so transpose
    cols.reverse()  # My brain works other way around than the cephalopod
    return cols


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()

    print(f"part 1: {step1(data)}")
    print(f"part 2: {step2(parse_2d_array(data))}")

assert step1(EXAMPLE) == 4277556
assert step2(parse_2d_array(EXAMPLE)) == 3263827
