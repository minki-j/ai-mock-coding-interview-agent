import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.rob([1, 2, 3, 1]), 4)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.rob([2, 7, 9, 3, 1]), 12)


if __name__ == "__main__":
    unittest.main()
