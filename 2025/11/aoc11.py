# %%
from functools import cache
from typing import Dict, Tuple
from collections import deque, defaultdict

Graph = Dict[str, Tuple[str]]

NODE_MASK = defaultdict(lambda: 0b00, {"dac": 0b01, "fft": 0b10})
ALL_MASK = 0b11


def part2(graph: Graph) -> int:
    @cache
    def dfs(node, state=0) -> int:
        if node == "out":
            return int(state == ALL_MASK)
        state |= NODE_MASK[node]
        return sum(dfs(child, state) for child in graph[node])

    return dfs("svr")


def part1(graph: Graph) -> int:
    q = deque(["you"])
    count = 0

    while q:  # bfs
        current = q.popleft()
        if current == "out":
            count += 1
        else:
            q.extend(graph[current])

    return count


def parse(text: str) -> Graph:
    graph = {}
    for line in text.splitlines():
        key, *vals = line.replace(":", "").split()
        graph[key] = tuple(vals)
    return graph


EXAMPLE = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

assert part1(parse(EXAMPLE)) == 5

if __name__ == "__main__":
    with open("input.txt") as f:
        graph = parse(f.read())
    print("Part1:", part1(graph))
    print("Part2:", part2(graph))
