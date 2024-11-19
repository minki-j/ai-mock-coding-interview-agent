import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome(121), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome(-121), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isPalindrome(10), False)


if __name__ == "__main__":
    unittest.main()
