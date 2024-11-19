import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(solution.majorityElement([3, 2, 3]), [3])


if __name__ == "__main__":
    unittest.main()
