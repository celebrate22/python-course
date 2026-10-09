class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        
        while left <= right:
            mid = (left + right)  // 2  # Finds the middle index
            
            if nums[mid] == target:
                return mid  # Target found
            elif nums[mid] < target:
                left = mid + 1  # Target is in the right half
            else:
                right = mid - 1  # Target is in the left half
                
        # If not found, 'left' will hold the correct insertion index
        return left
