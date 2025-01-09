from typing import List


class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        char_count = 0
        last_char = s[0]
        groups_list = []
        s += "1"
        for pos, char in enumerate(s):
            if last_char == char:
                char_count += 1
            else:
                if char_count > 2:
                    groups_list.append([pos - char_count, pos - 1])

                char_count = 1
                last_char = char

        return groups_list


sol = Solution()
print(sol.largeGroupPositions("aaa"))
