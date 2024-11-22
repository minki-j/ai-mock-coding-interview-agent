import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isValid("()"), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isValid("()[]{}"), True)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isValid("{[]}"), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isValid("(]"), False)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.isValid("([)]"), False)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.isValid("]"), False)


if __name__ == "__main__":
    unittest.main()
