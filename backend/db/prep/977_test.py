import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.sortedSquares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])


if __name__ == "__main__":
    unittest.main()
