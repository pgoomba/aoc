# %%

from collections import namedtuple
from typing import Tuple

Tree = namedtuple("Tree", ["width", "height", "counts"])


def parse(text: str):
    shapes = []
    shape = []
    trees = []
    for line in text.splitlines():
        if line.strip() == "":
            # shape done
            shapes.append(tuple(shape))
            shape = []
        elif line[-1] == ":":
            # new shape:
            assert len(shape) == 0
        elif line[-1] in ("#", "."):
            shape.append(tuple(c for c in line))
        else:  # space / package count
            first, *rest = line.replace(":", "").split(" ")
            width, height = map(int, first.split("x"))
            counts = tuple(map(int, rest))
            trees.append(Tree(width=width, height=height, counts=counts))

    return shapes, trees


def can_fit(shapes, tree: Tree) -> bool:
    # Can all the shapes fit side by side naively?
    max_shape_width = max([len(shape[0]) for shape in shapes])
    max_shape_height = max([len(shape) for shape in shapes])
    naive_fits = tree.width // max_shape_width * tree.height // max_shape_height
    brick_count = sum(tree.counts)

    if naive_fits >= brick_count:
        return True

    # If all the tiles could be packed perfectly without any gaps, would it still be too large?
    used_space_in_tile = [
        sum(cell == "#" for row in shape for cell in row) for shape in shapes
    ]
    perfect_packing_req = sum(
        used * count for used, count in zip(used_space_in_tile, tree.counts)
    )
    if perfect_packing_req > tree.width * tree.height:
        return False

    raise NotImplementedError("Add better bounds!")


def part1(shapes, trees: Tuple[Tree]):
    return sum(int(can_fit(shapes, tree)) for tree in trees)


EXAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip()

shapes, trees = parse(EXAMPLE)
# assert can_fit(shapes, trees[0])
assert can_fit(shapes, trees[1])
# assert can_fit(shapes, trees[2])

if __name__ == "__main__":
    with open("input.txt") as f:
        shapes, trees = parse(f.read())
    print("Part1:", part1(shapes, trees))  # type: ignore
