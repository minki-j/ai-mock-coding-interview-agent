from typing import List
import sys

sys.setrecursionlimit(10**9)
CACHE = {}


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
