import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.maxOperations([1, 2, 3, 4], 5), 2)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.maxOperations([3, 1, 3, 4, 3], 6), 1)


if __name__ == "__main__":
    unittest.main()
