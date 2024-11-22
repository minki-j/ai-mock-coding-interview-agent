import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.carPooling([[2, 1, 5], [3, 3, 7]], 4), False)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.carPooling([[2, 1, 5], [3, 3, 7]], 5), True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.carPooling([[2, 1, 5], [3, 5, 7]], 3), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(
            solution.carPooling([[7, 5, 6], [6, 7, 8], [10, 1, 6]], 16), False
        )

    def test_5(self):
        solution = Solution()
        self.assertEqual(
            solution.carPooling(
                [[8, 2, 3], [4, 1, 3], [1, 3, 6], [8, 4, 6], [4, 4, 8]], 12
            ),
            False,
        )


if __name__ == "__main__":
    unittest.main()
