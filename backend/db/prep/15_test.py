import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            {(frozenset(item)) for item in solution.threeSum([-1, 0, 1, 2, -1, -4])},
            {(frozenset(item)) for item in [[-1, -1, 2], [-1, 0, 1]]},
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.threeSum([]), [])

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.threeSum([0]), [])


if __name__ == "__main__":
    unittest.main()
