# import numpy as np
# from PIL import Image
# from matplotlib import pyplot as plt
#
# test=np.zeros((320,480),np.uint8)
#
# image = Image.fromarray(test)
# for i in range(330,338):
#     image.save('G:\AI-pycharm\Crack\CrackForest-dataset-master\groundTruthPngImg/%s.png'%(str(i)))
# print('ok')

class Solution:
    def canJump(self, nums):
        dp = [0] * len(nums)
        for i in range(1, len(nums)):
            dp[i] = max(dp[i - 1], nums[i - 1]) - 1
            if dp[i] < 0:
                return False
        return dp[-1] >= 0


solution = Solution()
# nums = [0]
# result = solution.canJump(nums)
# print(result)  # 输出True，因为可以跳到最后一个位置

nums = [3, 2, 1, 0, 4]
result = solution.canJump(nums)
print(result)  # 输出False，因为无法跳到最后一个位置