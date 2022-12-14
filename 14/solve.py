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
    filled = [[False for _ in range(0, 2000)] for _ in range(600)]
    low_level = 0
    for line in data:
        points = list(map(lambda x: list(map(int, x.split(","))), line.split(" -> ")))
        low_level = max(low_level, max(map(lambda x: x[1], points)))
        for i in range(len(points) - 1):
            dir = [np.sign(points[i + 1][0] - points[i][0]), np.sign(points[i + 1][1] - points[i][1])]
            cur = points[i]
            while cur[0] != points[i + 1][0] or cur[1] != points[i + 1][1]:
                filled[cur[0]][cur[1]] = True
                cur[0] += dir[0]
                cur[1] += dir[1]
            filled[cur[0]][cur[1]] = True


    assert not filled[500][0]

    ans = 0
    while True:
        cur = [500, 0]
        ok = False
        while cur[1] <= low_level:
            if not filled[cur[0]][cur[1] + 1]:
                cur[1] += 1
            elif not filled[cur[0] - 1][cur[1] + 1]:
                cur[0] -= 1
                cur[1] += 1
            elif not filled[cur[0] + 1][cur[1] + 1]:
                cur[0] += 1
                cur[1] += 1
            else:
                filled[cur[0]][cur[1]] = True
                ans += 1
                ok = True
                break
        if not ok:
            break

    submit(1, ans)

def part2():
    filled = [[False for _ in range(0, 2000)] for _ in range(1000)]
    low_level = 0
    for line in data:
        points = list(map(lambda x: list(map(int, x.split(","))), line.split(" -> ")))
        low_level = max(low_level, max(map(lambda x: x[1], points)))
        for i in range(len(points) - 1):
            dir = [np.sign(points[i + 1][0] - points[i][0]), np.sign(points[i + 1][1] - points[i][1])]
            cur = points[i]
            while cur[0] != points[i + 1][0] or cur[1] != points[i + 1][1]:
                filled[cur[0]][cur[1]] = True
                cur[0] += dir[0]
                cur[1] += dir[1]
            filled[cur[0]][cur[1]] = True

    assert not filled[500][0]

    ans = 1
    pending: list = [[500, 0]]
    filled[500][0] = True
    while len(pending) > 0:
        cur = pending.pop()
        if cur[1] >= low_level + 1: continue
        if not filled[cur[0]][cur[1] + 1]:
            filled[cur[0]][cur[1] + 1] = True
            pending.append([cur[0], cur[1] + 1])
            ans += 1
        if not filled[cur[0] - 1][cur[1] + 1]:
            filled[cur[0] - 1][cur[1] + 1] = True
            pending.append([cur[0] - 1, cur[1] + 1])
            ans += 1
        if not filled[cur[0] + 1][cur[1] + 1]:
            filled[cur[0] + 1][cur[1] + 1] = True
            pending.append([cur[0] + 1, cur[1] + 1])
            ans += 1

    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
