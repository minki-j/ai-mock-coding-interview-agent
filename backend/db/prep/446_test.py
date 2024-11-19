import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([2, 4, 6, 8, 10]), 7)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([2, 4, 6]), 1)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([2, 4]), 0)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([2, 4, 5, 6]), 2)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([2, 2, 3, 4]), 2)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 1, 2, 2, 3, 3]), 8)

    def test_7(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 1, 1, 1]), 3)

    def test_8(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 2, 3, 1, 2, 3]), 4)


if __name__ == "__main__":
    unittest.main()
