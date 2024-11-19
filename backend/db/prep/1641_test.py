import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.countVowelStrings(1), 5)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.countVowelStrings(2), 15)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.countVowelStrings(33), 66045)


if __name__ == "__main__":
    unittest.main()
