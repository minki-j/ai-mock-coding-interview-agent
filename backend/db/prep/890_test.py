import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            set(
                solution.findAndReplacePattern(
                    ["abc", "deq", "mee", "aqq", "dkd", "ccc"], "abb"
                )
            ),
            set(["mee", "aqq"]),
        )

    # @given(st.lists(st.integers(), min_size=1), st.lists(st.integers()))
    # def test_random(self, x, y):
    #     solution = Solution()
    #     self.assertEqual(solution.findAndReplacePattern(), True)


if __name__ == "__main__":
    unittest.main()
