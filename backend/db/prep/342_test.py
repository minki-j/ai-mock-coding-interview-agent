import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfFour(0), False)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfFour(4), True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfFour(16), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfFour(2445), False)


if __name__ == "__main__":
    unittest.main()
