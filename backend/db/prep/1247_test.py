import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.minimumSwap("xx", "yy"), 1)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.minimumSwap("xx", "xy"), -1)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.minimumSwap("xxyyxyxyxx", "xyyxyxxxyx"), 4)


if __name__ == "__main__":
    unittest.main()
