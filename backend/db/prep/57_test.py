import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.insert([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]])

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
            [[1, 2], [3, 10], [12, 16]],
        )

    def test_3(self):
        solution = Solution()
        self.assertEqual(
            solution.insert([[1, 5]], [0, 0]),
            [[0, 0], [1, 5]],
        )


if __name__ == "__main__":
    unittest.main()
