import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.findMaximumXOR([3, 10, 5, 25, 2, 8]), 28)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.findMaximumXOR([8, 10, 2]), 10)


if __name__ == "__main__":
    unittest.main()
