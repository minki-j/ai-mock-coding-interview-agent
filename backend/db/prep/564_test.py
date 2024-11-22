import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("123"), "121")

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("3"), "2")

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("11"), "9")

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("100"), "99")

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("1000"), "999")

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("9"), "8")

    def test_7(self):
        solution = Solution()
        self.assertEqual(solution.nearestPalindromic("99"), "101")

    def test_8(self):
        solution = Solution()
        self.assertEqual(
            solution.nearestPalindromic("807045053224792883"), "807045053350540708"
        )


if __name__ == "__main__":
    unittest.main()
