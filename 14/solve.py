#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
import numpy as np
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from init import get_session # type: ignore

def submit(part: int, ans):
    res = input(f"Submit answer {ans}? [Y/n]")
    if 'N' in res or 'n' in res: return
    day = int(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
    r = requests.post(f"https://adventofcode.com/2022/day/{day}/answer", data={"level": part, "answer": ans}, cookies={"session": get_session()})
    res = r.text
    print(res)
    print(res.split("\n")[-16])

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]

def part1():
    filled: set[tuple[int, int]] = set()
    low_level = 0
    for line in data:
        points = list(map(lambda x: np.array(list(map(int, x.split(",")))), line.split(" -> ")))
        low_level = max(low_level, max(map(lambda x: x[1], points)))
        for i in range(len(points) - 1):
            dir = (points[i + 1] - points[i]) // np.linalg.norm(points[i + 1] - points[i]).astype(int)
            cur = points[i]
            while np.any(cur != points[i + 1]):
                filled.add(tuple(cur))
                cur += dir
            filled.add(tuple(cur))

    assert (500, 0) not in filled

    ans = 0
    while True:
        cur = np.array([500, 0])
        ok = False
        while cur[1] <= low_level:
            if tuple(cur + np.array([0, 1])) not in filled:
                cur += np.array([0, 1])
            elif tuple(cur + np.array([-1, 1])) not in filled:
                cur += np.array([-1, 1])
            elif tuple(cur + np.array([1, 1])) not in filled:
                cur += np.array([1, 1])
            else:
                filled.add(tuple(cur))
                ans += 1
                ok = True
                break
        if not ok:
            break

    submit(1, ans)

def part2():
    filled: set[tuple[int, int]] = set()
    low_level = 0
    for line in data:
        points = list(map(lambda x: np.array(list(map(int, x.split(",")))), line.split(" -> ")))
        low_level = max(low_level, max(map(lambda x: x[1], points)))
        for i in range(len(points) - 1):
            dir = (points[i + 1] - points[i]) // np.linalg.norm(points[i + 1] - points[i]).astype(int)
            cur = points[i]
            while np.any(cur != points[i + 1]):
                filled.add(tuple(cur))
                cur += dir
            filled.add(tuple(cur))

    ans = 1
    pending: list = [np.array([500, 0])]
    filled.add((500, 0))
    while len(pending) > 0:
        cur = pending.pop()
        assert tuple(cur) in filled
        print(ans, cur)
        if cur[1] >= low_level + 1: continue
        if tuple(cur + np.array([0, 1])) not in filled:
            filled.add(tuple(cur + np.array([0, 1])))
            pending.append(cur + np.array([0, 1]))
            ans += 1
        if tuple(cur + np.array([-1, 1])) not in filled:
            filled.add(tuple(cur + np.array([-1, 1])))
            pending.append(cur + np.array([-1, 1]))
            ans += 1
        if tuple(cur + np.array([1, 1])) not in filled:
            filled.add(tuple(cur + np.array([1, 1])))
            pending.append(cur + np.array([1, 1]))
            ans += 1

    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
