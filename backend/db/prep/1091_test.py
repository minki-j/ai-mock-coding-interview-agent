import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.shortestPathBinaryMatrix([[0, 1], [1, 0]]), 2)

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]), 4
        )

    def test_3(self):
        solution = Solution()
        self.assertEqual(
            solution.shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]]), -1
        )

    def test_4(self):
        solution = Solution()
        self.assertEqual(
            solution.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 1]]), -1
        )

    def test_5(self):
        solution = Solution()
        self.assertEqual(
            solution.shortestPathBinaryMatrix([[0, 0, 0], [1, 0, 0], [1, 1, 0]]), 3
        )


if __name__ == "__main__":
    unittest.main()
