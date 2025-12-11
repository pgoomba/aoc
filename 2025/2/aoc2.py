from typing import List, Sequence, Tuple


def checkRange(rangeStr: str) -> Tuple[List[int], List[int]]:
    invalid1 = []
    invalid2 = []
    start, end = map(int, rangeStr.split("-"))

    for i in range(start, end + 1):
        s = str(i)
        s_len = len(s)

        # Part1, halves are the same:
        if (s_len % 2) == 0:
            mid = s_len // 2
            if s[:mid] == s[mid:]:
                invalid1.append(i)

        # Part2, repeated chunks:
        for n in range(1, s_len):
            if s_len % n != 0:
                continue
            if s[:n] * (s_len // n) == s:
                invalid2.append(i)
                break

    return invalid1, invalid2


def sumRanges(ranges: Sequence[str]) -> Tuple[int, int]:
    sum1 = sum2 = 0
    for r in ranges:
        invalid1, invalid2 = checkRange(r)
        sum1 += sum(invalid1)
        sum2 += sum(invalid2)
    return sum1, sum2


assert checkRange("11-22") == ([11, 22], [11, 22])
assert checkRange("95-115") == ([99], [99, 111])
assert checkRange("998-1012") == ([1010], [999, 1010])
assert checkRange("824824821-824824827") == ([], [824824824])

assert sumRanges(
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124".split(
        ","
    )
) == (1227775554, 4174379265)

with open("input.txt") as f:
    print(sumRanges(f.read().strip().split(",")))
