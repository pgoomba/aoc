from itertools import product

DIRECTIONS = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}

Grid = list[list[chr]]
Mask = list[list[int]]


def mask_rolls(grid: Grid) -> tuple[Mask, int]:
    rows = len(grid)
    cols = len(grid[0])
    output = [[0] * cols for _ in range(rows)]
    accessible = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "@":
                continue
            rolls = 0
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                    rolls += 1
            if rolls < 4:
                output[r][c] = 1
                accessible += 1
    return output, accessible


def remove_masked(grid: Grid, mask: Mask) -> Grid:
    return [
        ["." if m else cell for cell, m in zip(row, mask_row)]
        for row, mask_row in zip(grid, mask)
    ]


def step1(grid: Grid) -> int:
    _, count = mask_rolls(grid)
    return count


def step2(grid: Grid) -> int:
    current = grid
    removed = 0

    while (result := mask_rolls(current))[1] > 0:
        mask, count = result
        removed += count
        current = remove_masked(current, mask)

    return removed


EXAMPLE = [
    list(row)
    for row in [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
]

assert step1(EXAMPLE) == 13
assert step2(EXAMPLE) == 43

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        grid = [list(line.strip()) for line in f if line.strip()]
    print("Step 1:", step1(grid))
    print("Step 2:", step2(grid))
