import unittest
from statistics import median

import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([1, 3], [2]), 2)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([1, 2], [3, 4]), 2.5)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([2], []), 2)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([1, 2, 3, 4, 6], [5]), 3.5)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([1, 2], [-1, 3]), 1.5)

    def test_6(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([1, 3], [2, 7]), 2.5)

    def test_7(self):
        solution = Solution()
        self.assertEqual(solution.findMedianSortedArrays([2], [1, 3, 4]), 2.5)

    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    def test_random(self, x, y):
        solution = Solution()
        self.assertEqual(
            solution.findMedianSortedArrays(sorted(x), sorted(y)), median(sorted(x + y))
        )


if __name__ == "__main__":
    unittest.main()
