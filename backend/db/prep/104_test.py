import unittest

from utils.tree import make_tree


class Test(unittest.TestCase):
    def test_1(self):
        values = [3, 9, 20, None, None, 15, 7]
        root = make_tree(values)
        solution = Solution()
        self.assertEqual(solution.maxDepth(root), 3)

    def test_2(self):
        values = []
        root = make_tree(values)
        solution = Solution()
        self.assertEqual(solution.maxDepth(root), 0)

    def test_3(self):
        values = [0]
        root = make_tree(values)
        solution = Solution()
        self.assertEqual(solution.maxDepth(root), 1)


if __name__ == "__main__":
    unittest.main()
