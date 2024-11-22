import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([1, 2, 5], 11), 3)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([2], 3), -1)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([1], 0), 0)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([1], 1), 1)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([1], 2), 2)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.coinChange([1, 2, 4, 8, 10], 10002), 1001)

    # def test_7(self):
    #     solution = Solution()
    #     self.assertEqual(solution.coinChange([186, 419, 83, 408], 6249), 20)

    # @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    # def test_random(self, x, y):
    #     solution = Solution()
    #     self.assertEqual(solution.coinChange(), True)


if __name__ == "__main__":
    unittest.main()
