class Solution:     
    def longestCommonPrefix(self, strs: list[str]) -> str:                  
        longest_prefix = ""         
        for indx , word in enumerate(strs):             
            word = list(word)               
            
            # check each index in word starting from 0             
            # Note: Since the loop iterates over words, we look at the character 
            # at the current word's index across the first word for comparison.
            if indx < len(word) and strs[0][indx] == word[indx]:                 
                longest_prefix += word[indx]                              
            else:                 
                return longest_prefix          
        
        return longest_prefix  

strs = ["flower","flow","flight"]  
print(Solution().longestCommonPrefix(strs))

