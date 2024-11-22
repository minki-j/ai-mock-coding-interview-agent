import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.numMatchingSubseq("abcde", ["a", "bb", "acd", "ace"]), 3
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(
            solution.numMatchingSubseq(
                "qlhxagxdqh", ["qlhxagxdq", "qlhxagxdq", "lhyiftwtut", "yfzwraahab"]
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
