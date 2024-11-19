import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.merge([[1, 3], [2, 6], [8, 10], [15, 18]]),
            [[1, 6], [8, 10], [15, 18]],
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.merge([[1, 4], [4, 5]]), [[1, 5]])


if __name__ == "__main__":
    unittest.main()
