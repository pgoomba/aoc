from typing import Tuple

EXAMPLE = "\n".join(
    [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]
)


def tachyon_paths(grid_str: str) -> Tuple[int, int]:
    grid = [list(line) for line in grid_str.splitlines() if line.strip()]
    R, C = len(grid), len(grid[0])

    timelines = [[0] * C for _ in range(R)]
    timelines[0][grid[0].index("S")] = 1

    splits = 0

    for r in range(1, R):
        for c, source in enumerate(timelines[r - 1]):
            if source == 0:
                continue

            cell = grid[r][c]

            if cell == ".":
                timelines[r][c] += source
            elif cell == "^":
                splits += 1
                if c - 1 >= 0:
                    timelines[r][c - 1] += source
                if c + 1 < C:
                    timelines[r][c + 1] += source

    return (splits, sum(timelines[-1]))


with open("input.txt", "r") as f:
    data = f.read()
    print(tachyon_paths(data))

assert tachyon_paths(EXAMPLE) == (21, 40)
