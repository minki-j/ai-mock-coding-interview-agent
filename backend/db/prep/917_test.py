import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.reverseOnlyLetters("ab-cd"), "dc-ba")


if __name__ == "__main__":
    unittest.main()
