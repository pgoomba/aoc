# %%
from itertools import combinations, pairwise
from typing import List, Tuple

Coord = Tuple[int, int]


def parse(text: str) -> List[Coord]:
    return [tuple(map(int, line.split(","))) for line in text.splitlines()]


def rect_size(a: Coord, b: Coord) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def to_rect(a: Coord, b: Coord) -> Tuple[Coord, Coord, Coord, Coord]:
    return ((a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1]))


def is_inside(pt1: Coord, pt2: Coord, polygon: List[Coord]) -> bool:
    xmin, xmax = sorted((pt1[0], pt2[0]))
    ymin, ymax = sorted((pt1[1], pt2[1]))

    def between(a, b, x) -> bool:
        return a <= x <= b

    for (x1, y1), (x2, y2) in pairwise(polygon):
        # vertical:
        if x1 == x2:
            if xmin < x1 < xmax and (
                between(min(y1, y2), max(y1, y2), ymin)
                or between(min(y1, y2), max(y1, y2), ymax)
            ):
                return False

        # horizontal:
        elif y1 == y2:
            if ymin < y1 < ymax and (
                between(min(x1, x2), max(x1, x2), xmin)
                or between(min(x1, x2), max(x1, x2), xmax)
            ):
                return False

    return True


def part1(coords: List[Coord]) -> int:
    return max(rect_size(a, b) for a, b in combinations(coords, 2))


def part2(polygon: List[Coord]) -> int:
    # Polygon wraps, so insert first in last:
    polygon.append(polygon[0])
    return max(
        [
            rect_size(a, b)
            for a, b in combinations(polygon, 2)
            if is_inside(a, b, polygon)
        ]
    )


EXAMPLE = "\n".join(
    [
        "7,1",
        "11,1",
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3",
    ]
)


assert part1(parse(EXAMPLE)) == 50
assert part2(parse(EXAMPLE)) == 24

if __name__ == "__main__":
    with open("input.txt") as f:
        text = f.read()
        coords = parse(text)
        print(part1(coords))
        print(part2(coords))
