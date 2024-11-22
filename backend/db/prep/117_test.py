import unittest

from connect import Node, Solution


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        node7 = Node(7)
        node5 = Node(5)
        node4 = Node(4)
        node3 = Node(3, right=node7)
        node2 = Node(2, left=node4, right=node5)
        node1 = Node(1, left=node2, right=node3)
        root = solution.connect(node1)
        self.assertEqual(root.left.next, root.right)
        self.assertEqual(root.left.left.next, root.left.right)
        self.assertEqual(root.left.right.next, root.right.right)


if __name__ == "__main__":
    unittest.main()
