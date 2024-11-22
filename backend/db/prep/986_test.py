import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.intervalIntersection(
                [[0, 2], [5, 10], [13, 23], [24, 25]],
                [[1, 5], [8, 12], [15, 24], [25, 26]],
            ),
            [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]],
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.intervalIntersection(
                [[1, 3], [5, 9]],
                [],
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
