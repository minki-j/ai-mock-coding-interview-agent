import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.maxProfit([7, 1, 5, 3, 6, 4]), 5)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.maxProfit([7, 6, 4, 3, 1]), 0)


if __name__ == "__main__":
    unittest.main()
