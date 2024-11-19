import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.nthUglyNumber(10), 12)


if __name__ == "__main__":
    unittest.main()
