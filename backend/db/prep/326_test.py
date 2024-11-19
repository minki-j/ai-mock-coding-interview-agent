import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfThree(0), False)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfThree(9), True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfThree(243), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfThree(242), False)


if __name__ == "__main__":
    unittest.main()
