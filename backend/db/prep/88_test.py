import unittest
import hypothesis.strategies as st
from hypothesis import given


class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        nums1 = [1, 2, 3, 0, 0, 0]
        nums2 = [2, 5, 6]
        solution.merge(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [1, 2, 2, 3, 5, 6])

    def test_2(self):
        solution = Solution()
        nums1 = [0]
        nums2 = [1]
        solution.merge(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [1])

    def test_3(self):
        solution = Solution()
        nums1 = [0, 0]
        nums2 = [0, 1]
        solution.merge(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [0, 1])

    def test_4(self):
        solution = Solution()
        nums1 = [1]
        nums2 = []
        solution.merge(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [1])

    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_random(self, nums1, nums2):
        solution = Solution()
        nums1 = sorted(nums1)
        nums2 = sorted(nums2)
        nums1_sorted = sorted(nums1 + nums2)
        nums1 += [0] * len(nums2)
        solution.merge(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, nums1_sorted)


if __name__ == "__main__":
    unittest.main()
