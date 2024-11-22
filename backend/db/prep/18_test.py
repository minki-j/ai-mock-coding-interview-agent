import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        expected = set(
            [tuple(sorted(i)) for i in [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]]
        )
        result = set(
            [tuple(sorted(i)) for i in solution.fourSum([1, 0, -1, 0, -2, 2], 0)]
        )
        self.assertEqual(result, expected)

    @given(st.lists(st.integers()), st.integers())
    def test_random(self, nums, target):
        solution = Solution()
        expected = set([tuple(sorted(i)) for i in solution.fourSumNaive(nums, target)])
        result = set([tuple(sorted(i)) for i in solution.fourSum(nums, target)])
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
