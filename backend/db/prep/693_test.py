import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.hasAlternatingBits(5), True)


if __name__ == "__main__":
    unittest.main()