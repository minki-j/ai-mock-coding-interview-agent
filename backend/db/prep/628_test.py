import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.maximumProduct([1, 2, 3]), 6)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.maximumProduct([-2, -2, -1]), -4)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.maximumProduct([0, 1, 1, 1]), 1)

    @given(st.lists(st.integers(), min_size=3))
    def test_random(self, nums):
        solution = Solution()
        self.assertEqual(
            solution.maximumProduct(nums), solution.maximumProductNaive(nums)
        )


if __name__ == "__main__":
    unittest.main()
