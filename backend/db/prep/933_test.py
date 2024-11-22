import unittest

from recent_counter import RecentCounter


class Test(unittest.TestCase):
    def test_1(self):
        obj = RecentCounter()
        results = [obj.ping(t) for t in [1, 100, 3001, 3002]]
        self.assertEqual(results, [1, 2, 3, 3])


if __name__ == "__main__":
    unittest.main()
