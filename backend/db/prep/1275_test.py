import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.tictactoe([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]]), "A"
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.tictactoe([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]]), "B"
        )

    def test_3(self):
        solution = Solution()
        self.assertEqual(
            solution.tictactoe(
                [[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]]
            ),
            "Draw",
        )

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.tictactoe([[0, 0], [1, 1]]), "Pending")


if __name__ == "__main__":
    unittest.main()
