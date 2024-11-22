import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isOneBitCharacter([1, 0, 0]), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isOneBitCharacter([1, 1, 1, 0]), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isOneBitCharacter([0, 1, 1, 1, 0]), False)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isOneBitCharacter([0]), True)

    @given(st.lists(st.sampled_from(["0", "10", "11"]), min_size=1))
    def test_random(self, bits):
        result = bits[-1] == "0"
        bits = [int(bit) for bit in "".join(bits)]
        solution = Solution()
        self.assertEqual(solution.isOneBitCharacter(bits), result)


if __name__ == "__main__":
    unittest.main()
