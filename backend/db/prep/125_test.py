import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome("A man, a plan, a canal: Panama"), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome("race a car"), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome(" "), True)


if __name__ == "__main__":
    unittest.main()
