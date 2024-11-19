import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.sequentialDigits(100, 300), [123, 234])

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.sequentialDigits(1000, 13000),
            [1234, 2345, 3456, 4567, 5678, 6789, 12345],
        )


if __name__ == "__main__":
    unittest.main()
