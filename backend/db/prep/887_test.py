import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(1, 1), 1)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(1, 10), 10)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(3, 1), 1)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(2, 6), 3)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(2, 7), 4)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(3, 14), 4)

    def test_8(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(2, 2), 2)

    def test_9(self):
        solution = Solution()
        self.assertEqual(solution.superEggDrop(2, 4), 3)


if __name__ == "__main__":
    unittest.main()
