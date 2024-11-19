import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.arrayStringsAreEqual(["ab", "c"], ["a", "bc"]), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.arrayStringsAreEqual(["ab", "c"], ["a", "cb"]), False)


if __name__ == "__main__":
    unittest.main()
