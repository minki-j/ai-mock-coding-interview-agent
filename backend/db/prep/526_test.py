import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.countArrangement(1), 1)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.countArrangement(2), 2)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.countArrangement(3), 3)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.countArrangement(4), 8)


if __name__ == "__main__":
    unittest.main()
