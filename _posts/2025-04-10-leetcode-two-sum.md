---
title: "Two Sum"
date: 2025-04-10 00:00:00 +0900
categories: [Algorithm, LeetCode]
tags: ["array", "hash-table"]
image:
  path: /assets/img/algorithm/leetcode/two-sum.png
  alt: "Two Sum"
---

# 목표  : nums안의 숫자 두개를 더한 값이 target이 되는 두 인덱스 값을 찾기
## nums배열을 순회하면서 target-nums[i]가 dic안에 있는지 확인하면 된다

## 풀이 코드

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        n = len(nums)
        for i in range(n):
            if target - nums[i] in dic:
                return [dic[target-nums[i]],i]
            
            else :
                dic[nums[i]] = i
```
