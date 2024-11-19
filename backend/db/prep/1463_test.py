import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.cherryPickup([[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]]),
            24,
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.cherryPickup(
                [
                    [1, 0, 0, 0, 0, 0, 1],
                    [2, 0, 0, 0, 0, 3, 0],
                    [2, 0, 9, 0, 0, 0, 0],
                    [0, 3, 0, 5, 4, 0, 0],
                    [1, 0, 2, 3, 0, 0, 6],
                ]
            ),
            28,
        )

    def test_3(self):
        solution = Solution()
        self.assertEqual(
            solution.cherryPickup(
                [[1, 0, 0, 3], [0, 0, 0, 3], [0, 0, 3, 3], [9, 0, 3, 3]]
            ),
            22,
        )

    def test_4(self):
        solution = Solution()
        self.assertEqual(
            solution.cherryPickup([[1, 1], [1, 1]]),
            4,
        )

    def test_5(self):
        solution = Solution()
        self.assertEqual(
            solution.cherryPickup(
                [
                    [8, 8, 10, 9, 1, 7],
                    [8, 8, 1, 8, 4, 7],
                    [8, 6, 10, 3, 7, 7],
                    [3, 0, 9, 3, 2, 7],
                    [6, 8, 9, 4, 2, 5],
                    [1, 1, 5, 8, 8, 1],
                    [5, 6, 5, 2, 9, 9],
                    [4, 4, 6, 2, 5, 4],
                    [4, 4, 5, 3, 1, 6],
                    [9, 2, 2, 1, 9, 3],
                ]
            ),
            146,
        )


if __name__ == "__main__":
    unittest.main()
