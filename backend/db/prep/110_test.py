import unittest

from utils.tree import make_tree


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        values = [3, 9, 20, None, None, 15, 7]
        root = make_tree(values)
        self.assertEqual(solution.isBalanced(root), True)

    def test_2(self):
        solution = Solution()
        values = [1, 2, 2, 3, 3, None, None, 4, 4]
        root = make_tree(values)
        self.assertEqual(solution.isBalanced(root), False)

    def test_3(self):
        solution = Solution()
        values = []
        root = make_tree(values)
        self.assertEqual(solution.isBalanced(root), True)


if __name__ == "__main__":
    unittest.main()
