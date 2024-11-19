import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            set(solution.commonChars(["bella", "label", "roller"])),
            set(["e", "l", "l"]),
        )


if __name__ == "__main__":
    unittest.main()
