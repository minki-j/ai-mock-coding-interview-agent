import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isRobotBounded("GGLLGG"), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isRobotBounded("GG"), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isRobotBounded("GL"), True)


if __name__ == "__main__":
    unittest.main()
