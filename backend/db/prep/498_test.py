import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.findDiagonalOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            [1, 2, 4, 7, 5, 3, 6, 8, 9],
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.findDiagonalOrder([[]]),
            [],
        )

    def test_3(self):
        solution = Solution()
        self.assertEqual(
            solution.findDiagonalOrder([[1, 2, 3], [4, 5, 6]]),
            [1, 2, 4, 5, 3, 6],
        )

    def test_4(self):
        solution = Solution()
        self.assertEqual(
            solution.findDiagonalOrder([[1, 2], [4, 5], [7, 8]]),
            [1, 2, 4, 7, 5, 8],
        )

    def test_4(self):
        solution = Solution()
        self.assertEqual(
            solution.findDiagonalOrder([]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
