import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.breakPalindrome("abccba"), "aaccba")

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.breakPalindrome("a"), "")

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.breakPalindrome("aaa"), "aab")

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.breakPalindrome("aba"), "abb")


if __name__ == "__main__":
    unittest.main()
