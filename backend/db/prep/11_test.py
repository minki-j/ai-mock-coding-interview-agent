import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.maxArea([1, 1]), 1)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.maxArea([4, 3, 2, 1, 4]), 16)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.maxArea([1, 2, 1]), 2)

    @given(st.lists(st.integers(min_value=0), min_size=2))
    def test_random(self, height):
        solution = Solution()
        self.assertEqual(solution.maxArea(height), solution.maxAreaNaive(height))


if __name__ == "__main__":
    unittest.main()
