import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        nums = [1, 2, 3]
        solution.nextPermutation(nums)
        self.assertEqual(nums, [1, 3, 2])

    def test_2(self):
        solution = Solution()
        nums = [3, 2, 1]
        solution.nextPermutation(nums)
        self.assertEqual(nums, [1, 2, 3])

    def test_3(self):
        solution = Solution()
        nums = [1, 3, 2]
        solution.nextPermutation(nums)
        self.assertEqual(nums, [2, 1, 3])


if __name__ == "__main__":
    unittest.main()
