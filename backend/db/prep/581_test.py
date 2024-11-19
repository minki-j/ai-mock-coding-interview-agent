import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.findUnsortedSubarray([2, 6, 4, 8, 10, 9, 15]), 5)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.findUnsortedSubarray([1]), 0)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.findUnsortedSubarray([1, 2, 3, 4]), 0)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.findUnsortedSubarray([2, 1]), 2)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.findUnsortedSubarray([0, -1]), 2)

    @given(st.lists(st.integers(), min_size=1))
    def test_random(self, nums):
        solution = Solution()
        self.assertEqual(
            solution.findUnsortedSubarray(nums),
            solution.findUnsortedSubarrayNaive(nums),
        )


if __name__ == "__main__":
    unittest.main()
