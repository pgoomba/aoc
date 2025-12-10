# %%
from collections import deque
from dataclasses import dataclass
from typing import List
import pulp

EXAMPLE = "\n".join(
    [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
    ]
)


@dataclass
class Machine:
    lights: List[bool]
    buttons: List[int]
    joltage: List[int]

    def target_mask(self) -> int:
        target = 0
        for i, on in enumerate(self.lights):
            if on:
                target |= 1 << i
        return target

    def button_masks(self) -> List[int]:
        btn_masks = []
        for btn in self.buttons:
            mask = 0
            for bit in btn:
                mask |= 1 << bit
            btn_masks.append(mask)
        return btn_masks

    def button_ints(self) -> List[int]:
        btn_ints = []
        for btn in self.buttons:
            ints = [0] * len(self.lights)
            for light in btn:
                ints[light] = 1
            btn_ints.append(ints)
        return btn_ints


def part1_min_presses(machine: Machine) -> int:
    target = machine.target_mask()
    btn_masks = machine.button_masks()

    start = 0
    if start == target:
        return 0

    # BFS
    q = deque([(start, 0)])
    seen = {start}

    while q:
        state, dist = q.popleft()
        for mask in btn_masks:
            toggled = state ^ mask
            if toggled == target:
                return dist + 1
            if toggled not in seen:
                seen.add(toggled)
                q.append((toggled, dist + 1))

    assert False, "How did we get here?"


def part1(machines: List[Machine]) -> int:
    return sum(map(part1_min_presses, machines))


def parse(text: str) -> List[Machine]:
    machines = []
    for line in text.splitlines():
        buttons = []
        joltage = []
        lights = []
        for word in line.split(" "):
            if word[0] == "[":
                assert len(lights) == 0
                lights = [x == "#" for x in word[1:-1]]
            if word[0] == "(":
                buttons.append(tuple([int(x) for x in word[1:-1].split(",")]))
            if word[0] == "{":
                assert len(joltage) == 0
                joltage = [int(x) for x in word[1:-1].split(",")]
        machines.append(Machine(lights=lights, buttons=buttons, joltage=joltage))
    return machines


def part2_cop_out_via_linear_solver(machine: Machine) -> int:
    target = machine.joltage
    btn_ints = machine.button_ints()
    n_btn = len(btn_ints)
    n_lights = len(target)

    x = [pulp.LpVariable(f"x{i}", 0, cat="Integer") for i in range(n_btn)]
    problem = pulp.LpProblem("Min button presses for joltage", pulp.LpMinimize)
    problem += pulp.lpSum(x)

    for light_idx in range(n_lights):
        problem += (
            pulp.lpSum(btn_ints[j][light_idx] * x[j] for j in range(n_btn))
            == target[light_idx]
        )

    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    return int(sum(v.value() for v in x))


def part2(machines: List[Machine]):
    return sum(map(part2_cop_out_via_linear_solver, machines))


example = parse(EXAMPLE)
assert part1(example) == 7
assert part2(example) == 33

if __name__ == "__main__":
    with open("input.txt") as f:
        text = f.read()
        machines = parse(text)
        print("Part1:", part1(machines))
        print("Part2:", part2(machines))

# %%
