#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <cassert>

int64_t best(const std::string &input, int32_t k)
{
    std::vector<uint8_t> digits;
    digits.reserve(input.size());
    for (char c : input)
    {
        digits.emplace_back(c - '0');
    }
    size_t n = digits.size();
    // dp[i][j]: largest number by selecting j digits from first i digits
    std::vector<std::vector<int64_t>> dp(n + 1, std::vector<int64_t>(k + 1, 0));

    for (size_t i = 1; i <= n; ++i)
    {
        for (size_t j = 1; j <= std::min(i, static_cast<size_t>(k)); ++j)
        {
            dp[i][j] = std::max(
                dp[i - 1][j],                           // Leave the current digit
                dp[i - 1][j - 1] * 10 + digits[i - 1]); // Grab current
        }
    }
    return dp[n][k];
}

int main()
{
    assert(best("987654321111111", 2) == 98);
    assert(best("811111111111119", 2) == 89);
    assert(best("987654321111111", 12) == 987654321111);
    assert(best("811111111111119", 12) == 811111111119);
    assert(best("234234234234278", 12) == 434234234278);

    int64_t part1 = 0, part2 = 0;
    std::ifstream fin("input.txt");
    std::string line;
    while (std::getline(fin, line))
    {
        part1 += best(line, 2);
        part2 += best(line, 12);
    }
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    return 0;
}
