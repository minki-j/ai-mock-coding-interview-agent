import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.subtractProductAndSum(234), 15)


if __name__ == "__main__":
    unittest.main()
