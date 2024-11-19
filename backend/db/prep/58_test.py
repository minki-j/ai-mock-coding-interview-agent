import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLastWord("a"), 1)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLastWord(" "), 0)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLastWord("Hello World"), 5)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.lengthOfLastWord("a "), 1)


if __name__ == "__main__":
    unittest.main()
