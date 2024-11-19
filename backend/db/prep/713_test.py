import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.numSubarrayProductLessThanK([10, 5, 2, 6], 100), 8)


if __name__ == "__main__":
    unittest.main()
