import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.findPoisonedDuration([1, 4], 2), 4)


if __name__ == "__main__":
    unittest.main()
