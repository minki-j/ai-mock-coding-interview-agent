import unittest

# import hypothesis.strategies as st
# from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.longestPalindrome("babad") in ["bab", "aba"], True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.longestPalindrome("cbbd") in ["bb"], True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.longestPalindrome("a") in ["a"], True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.longestPalindrome("ac") in ["a", "c"], True)

    # @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    # def test_random(self, x, y):
    #     solution = Solution()
    #     self.assertEqual(solution.longestPalindrome(), True)


if __name__ == "__main__":
    unittest.main()
