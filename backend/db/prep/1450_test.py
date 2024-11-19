import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.busyStudent([1, 2, 3], [3, 2, 7], 4), 1)


if __name__ == "__main__":
    unittest.main()
