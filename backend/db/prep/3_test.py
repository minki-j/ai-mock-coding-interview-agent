import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLongestSubstring("abcabcbb"), 3)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLongestSubstring("dvdf"), 3)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLongestSubstring("aabaab!bb"), 3)


if __name__ == "__main__":
    unittest.main()
