import unittest

# import hypothesis.strategies as st
# from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 2, 3, 4]), 3)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 2, 3]), 1)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 2]), 0)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.numberOfArithmeticSlices([1, 2, 5, 7, 9]), 1)

    # @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    # def test_random(self, x, y):
    #     solution = Solution()
    #     self.assertEqual(solution.numberOfArithmeticSlices(), True)


if __name__ == "__main__":
    unittest.main()
