import unittest

from utils.tree import make_tree


class Test(unittest.TestCase):
    def test_1(self):
        values = [1, None, 2, 3]
        root = make_tree(values)
        solution = Solution()
        self.assertEqual(solution.inorderTraversal(root), [1, 3, 2])

    def test_2(self):
        solution = Solution()
        self.assertEqual(solution.inorderTraversal(None), [])


if __name__ == "__main__":
    unittest.main()
