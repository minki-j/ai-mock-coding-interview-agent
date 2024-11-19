import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.maxProduct([2, 3, -2, 4]), 6)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.maxProduct([-2, 0, -1]), 0)

    # @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    # def test_random(self, x, y):
    #     solution = Solution()
    #     self.assertEqual(solution.maxProduct(), True)


if __name__ == "__main__":
    unittest.main()
