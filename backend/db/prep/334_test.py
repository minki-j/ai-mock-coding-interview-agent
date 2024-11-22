import unittest

import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.increasingTriplet([1, 2, 3, 4, 5]), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.increasingTriplet([5, 4, 3, 2, 1]), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.increasingTriplet([2, 1, 5, 0, 4, 6]), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.increasingTriplet([0, 4, 2, 1, 0, -1, -3]), False)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.increasingTriplet([5, 6, 3, 4, 1, 2]), False)

    @given(st.lists(st.integers()))
    def test_random(self, nums):
        solution = Solution()
        self.assertEqual(
            solution.increasingTriplet(nums), solution.increasingTripletNaive(nums)
        )


if __name__ == "__main__":
    unittest.main()
