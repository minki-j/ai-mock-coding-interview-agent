import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            solution.minJumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]), 3
        )

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.minJumps([7]), 0)

    def test_3(self):
        solution = Solution()
        self.assertEqual(solution.minJumps([7, 6, 9, 6, 9, 6, 9, 7]), 1)

    def test_4(self):
        solution = Solution()
        self.assertEqual(solution.minJumps([6, 1, 9]), 2)

    def test_5(self):
        solution = Solution()
        self.assertEqual(solution.minJumps([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13]), 3)

    def test_6(self):
        solution = Solution()
        self.assertEqual(
            solution.minJumps(
                [-76, 3, 66, -32, 64, 2, -19, -8, -5, -93, 80, -5, -76, -78, 64, 2, 16]
            ),
            5,
        )

    def test_7(self):
        solution = Solution()
        self.assertEqual(solution.minJumps([7] * (5 * 10**4) + [11]), 2)

    def test_8(self):
        solution = Solution()
        self.assertEqual(
            solution.minJumps(
                [7, 6, 8, 6, 8, 6, 8, 6, 8, 6, 8, 6, 8, 8, 8, 6, 6, 5, 6]
                + [7] * (5 * 10**4)
                + [8, 6, 8, 6, 7]
                + [11]
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
