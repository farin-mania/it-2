from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        if nums[0] > target: return 0
        left, right = 0, len(nums) - 1

        while left <= right: 
            mid = (left + right) // 2
            print(mid, left, right)

            match nums[mid]:
                case x if x < target: 
                    left = mid + 1
                case x if x > target: 
                    right = mid - 1
                case target: return mid

        return left

                    

print(Solution().searchInsert([1,3,5,6], 4))