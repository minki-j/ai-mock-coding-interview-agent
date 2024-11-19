import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isIsomorphic("egg", "add"), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isIsomorphic("foo", "bar"), False)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.isIsomorphic("paper", "title"), True)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.isIsomorphic("ab", "aa"), False)


if __name__ == "__main__":
    unittest.main()
