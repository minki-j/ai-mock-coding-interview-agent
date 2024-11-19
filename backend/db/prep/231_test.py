import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfTwo(0), False)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfTwo(2), True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfTwo(8), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isPowerOfTwo(9), False)


if __name__ == "__main__":
    unittest.main()
