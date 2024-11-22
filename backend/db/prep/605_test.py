import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([1, 0, 0, 0, 1], 1), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([1, 0, 0, 0, 1], 2), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([1, 0, 0, 0, 0, 1], 2), False)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([1, 0, 0, 0, 0, 0, 1], 2), True)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([1, 0, 0, 0, 0, 0, 1], 3), False)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([0, 0, 1, 0, 1], 1), True)

    def test_7(self):
        solution = Solution()
        self.assertEqual(solution.canPlaceFlowers([0, 0, 1, 0, 1][::-1], 1), True)


if __name__ == "__main__":
    unittest.main()
