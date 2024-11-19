import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.reachingPoints(1, 1, 3, 5), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.reachingPoints(1, 1, 2, 2), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.reachingPoints(1, 1, 1, 1), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.reachingPoints(1, 1, 10**9, 1), True)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.reachingPoints(9, 5, 12, 8), False)

    @given(st.lists(st.integers(min_value=1, max_value=100), min_size=4, max_size=4))
    def test_random(self, array):
        sx, sy, tx, ty = array
        solution = Solution()
        self.assertEqual(
            solution.reachingPoints(sx, sy, tx, ty),
            solution.reachingPointsNaive(sx, sy, tx, ty),
        )


if __name__ == "__main__":
    unittest.main()
