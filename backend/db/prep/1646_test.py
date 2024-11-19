import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.getMaximumGenerated(2), 1)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.getMaximumGenerated(7), 3)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.getMaximumGenerated(3), 2)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.getMaximumGenerated(0), 0)


if __name__ == "__main__":
    unittest.main()
