import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.wiggleMaxLength([1, 17, 5, 10, 13, 15, 10, 5, 16, 8]), 7
        )


if __name__ == "__main__":
    unittest.main()
