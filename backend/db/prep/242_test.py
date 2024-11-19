import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.isAnagram("anagram", "nagaram"), True)

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.isAnagram("rat", "car"), False)


if __name__ == "__main__":
    unittest.main()
