from typing import List


class Solution:
    def trimMean(self, arr: List[int]) -> float:
        trimmed = self.trim_extremes(arr)
        print(trimmed)

        return sum(trimmed) / len(trimmed)

    def trim_extremes(self, numbers):
        if len(numbers) < 20:
            return numbers

        sorted_nums = sorted(numbers)
        cutoff = int(len(numbers) * 0.05)
        return sorted_nums[cutoff:-cutoff]


print(Solution().trimMean([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]))
