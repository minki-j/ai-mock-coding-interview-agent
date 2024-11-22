import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.longestCommonPrefix(["flower", "flow", "flight"]), "fl"
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.longestCommonPrefix(["dog", "racecar", "car"]), "")


if __name__ == "__main__":
    unittest.main()
