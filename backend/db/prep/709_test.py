import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.toLowerCase("Hello"), "hello")

    @given(st.text())
    def test_random(self, s):
        solution = Solution()
        self.assertEqual(solution.toLowerCase(s), s.lower())


if __name__ == "__main__":
    unittest.main()
