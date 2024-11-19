import unittest

# import hypothesis.strategies as st
# from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.sortArrayByParity([3, 4, 1, 2]), [4, 2, 3, 1])


if __name__ == "__main__":
    unittest.main()
