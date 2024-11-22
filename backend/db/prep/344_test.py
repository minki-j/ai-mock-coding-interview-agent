import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        s = ["a", "b", "c"]
        solution.reverseString(s)
        self.assertEqual(s, ["c", "b", "a"])


if __name__ == "__main__":
    unittest.main()
