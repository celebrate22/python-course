class Solution:
    def __init__(self, nums: list[int], target: int) -> list[int]:

        self.nums = nums
        self.target = target
    def twoSum(self):
        num_to_index = {}
        
        for index, num in enumerate(self.nums):
            complement = self.target - num
            if complement in num_to_index:
                return [num_to_index[complement], index]
            num_to_index[num] = index
            
        return []

target = 10

nums = [4,7,8,6]

soln = Solution(nums, target)

print(soln.twoSum())