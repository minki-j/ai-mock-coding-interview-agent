import random
import string
import unittest

from hypothesis import given
from hypothesis.strategies import text


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.findTheDifference("abcd", "abcde"), "e")

    @given(text())
    def test_random(self, s):
        solution = Solution()
        random_letter = random.choice(string.ascii_letters)
        t = list(s + random_letter)
        random.shuffle(t)
        t = "".join(t)
        self.assertEqual(solution.findTheDifference(s, t), random_letter)


if __name__ == "__main__":
    unittest.main()
