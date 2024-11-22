import unittest
import copy
import hypothesis.strategies as st
from hypothesis import given
from utils.linked_list import make_linked_list, linked_list_to_list


class Test(unittest.TestCase):
    def test_1(self):
        values = [1, 2, 3, 4]
        head = make_linked_list(values)
        ori_head = copy.deepcopy(head)
        solution = Solution()
        swap_head = solution.swapPairs(head)
        head = ori_head
        self.assertEqual(head.val, swap_head.next.val)
        self.assertEqual(head.next.val, swap_head.val)

    def test_2(self):
        values = [1, 2, 3]
        head = make_linked_list(values)
        ori_head = copy.deepcopy(head)
        solution = Solution()
        swap_head = solution.swapPairs(head)
        head = ori_head
        self.assertEqual(head.next.next.val, swap_head.next.next.val)

    def test_3(self):
        values = [1]
        head = make_linked_list(values)
        ori_head = copy.deepcopy(head)
        solution = Solution()
        swap_head = solution.swapPairs(head)
        head = ori_head
        self.assertEqual(head.val, swap_head.val)

    @given(st.lists(st.integers()))
    def test_random(self, values):
        head = make_linked_list(values)
        solution = Solution()
        swap_head = solution.swapPairs(head)
        swap_values = linked_list_to_list(swap_head)
        for i in range(0, len(swap_values) - 1, 2):
            swap_values[i], swap_values[i + 1] = (
                swap_values[i + 1],
                swap_values[i],
            )
        self.assertEqual(values, swap_values)


if __name__ == "__main__":
    unittest.main()
