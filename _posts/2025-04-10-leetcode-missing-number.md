---
title: "Missing Number"
date: 2025-04-10 00:00:00 +0900
categories: [Algorithm, LeetCode]
tags: []
image:
  path: /assets/img/algorithm/leetcode/missing-number.png
  alt: "Missing Number"
---

## 풀이 코드

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            n ^= i ^ nums[i]

        return n
```
