from typing import Tuple, List
from itertools import combinations
from collections import defaultdict
import math
import heapq


Coord = Tuple[int, int, int]


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


def parse(text: str) -> List[Coord]:
    return [tuple(map(int, line.split(","))) for line in text.strip().splitlines()]


def min_dist_heap(coords: List[Coord]) -> List[Tuple[float, Coord, Coord]]:
    queue = []
    for a, b in combinations(coords, 2):
        dist = math.dist(a, b)
        heapq.heappush(queue, (dist, a, b))
    return queue


def mul_largest_3(uf: UnionFind, coords: List[Coord]) -> int:
    components = defaultdict(int)
    for i in range(len(coords)):
        root = uf.find(i)
        components[root] += 1

    largest_3 = sorted(components.values(), reverse=True)[:3]
    return math.prod(largest_3)


def solve(coords: List[Coord], n_connections: int) -> Tuple[int, int]:
    index = {coord: i for i, coord in enumerate(coords)}
    queue = min_dist_heap(coords)

    uf = UnionFind(len(coords))
    edges_used = 0
    part1 = 0
    part2 = 0

    while queue and uf.components > 1:
        dist, a, b = heapq.heappop(queue)
        ia, ib = index[a], index[b]
        uf.union(ia, ib)
        edges_used += 1

        if edges_used == n_connections:
            part1 = mul_largest_3(uf, coords)
        if uf.components == 1:  # Assumes part2 need more connections than part1
            part2 = a[0] * b[0]

    return (part1, part2)


EXAMPLE = "\n".join(
    [
        "162,817,812",
        "57,618,57",
        "906,360,560",
        "592,479,940",
        "352,342,300",
        "466,668,158",
        "542,29,236",
        "431,825,988",
        "739,650,466",
        "52,470,668",
        "216,146,977",
        "819,987,18",
        "117,168,530",
        "805,96,715",
        "346,949,466",
        "970,615,88",
        "941,993,340",
        "862,61,35",
        "984,92,344",
        "425,690,689",
    ]
)

assert solve(parse(EXAMPLE), 10) == (40, 25272)

if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()
    coords = parse(input)
    print(solve(coords, 1000))
