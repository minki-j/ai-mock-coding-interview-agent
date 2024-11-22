import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.reverseWords("Let's take LeetCode contest"),
            "s'teL ekat edoCteeL tsetnoc",
        )


if __name__ == "__main__":
    unittest.main()
