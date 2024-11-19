import unittest


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        node1 = Node(1, None, None)
        node2 = Node(2, None, None)
        node1.next = node2
        node1.random = node2
        node2.random = node2
        new_head = solution.copyRandomList(node1)
        self.assertEqual(new_head.val, 1)
        self.assertEqual(new_head.next.val, 2)
        self.assertEqual(new_head.random is not node2, True)
        self.assertEqual(new_head.random is not None, True)
        self.assertEqual(new_head.next.random is not node2, True)
        self.assertEqual(new_head.next.random is not None, True)


if __name__ == "__main__":
    unittest.main()
