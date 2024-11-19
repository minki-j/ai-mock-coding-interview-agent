import unittest




class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.distributeCandies(5, 2), 3)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.distributeCandies(3, 3), 10)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.distributeCandies(6, 1), 0)


if __name__ == "__main__":
    unittest.main()
