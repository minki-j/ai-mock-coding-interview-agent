import unittest
class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.twoSum(nums = [2,7,11,15], target = 9), [0,1])
        
    def test_2(self):
        solution = Solution()\n        self.assertEqual(solution.twoSum(nums = [3,2,4], target = 6), [1,2])\n    def test_3(self):\n        solution = Solution()\n        self.assertEqual(solution.twoSum(nums = [3,3], target = 6), [0,1])\n\nif __name__ == \"__main__\":\n    unittest.main()\n