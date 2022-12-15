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
    parsed = list(map(lambda x: list(map(int, x)), map(lambda y: [y[1].split(", y=")[0], y[1].split(", y=")[1].split(":")[0], *y[2].split(", y=")], map(lambda x: x.split("x="), data))))

def part1():
    ranges: list[tuple[int, int]] = []
    for line in parsed:
        dist = abs(line[0] - line[2]) + abs(line[1] - line[3])
        vdist = abs(line[1] - 2000000)
        if dist >= vdist:
            delta = dist - vdist
            ranges.append((line[0] - delta, line[0] + delta + 1))
    ranges = list(sorted(ranges))
    ans = 0
    cur_last = ranges[0][0]
    for r in ranges:
        if r[0] > cur_last:
            cur_last = r[0]
        if r[1] <= cur_last:
            continue
        ans += r[1] - cur_last
        cur_last = r[1]
    existing = set(x[2] for x in parsed if x[3] == 2000000)
    submit(1, ans - len(existing))

def test_beacon(x: int, y: int):
    if not 0 <= x <= 4000000: return False
    if not 0 <= y <= 4000000: return False
    for line in parsed:
        disto = abs(line[0] - line[2]) + abs(line[1] - line[3])
        distn = abs(line[0] - x) + abs(line[1] - y)
        if distn <= disto:
            return False
    print("Found:", x, y)
    return True

def part2():
    possible = {line[1] for line in parsed}
    possible.add(0)
    possible.add(4000000)
    good_h = -1
    result = 0
    while True:
        ranges: list[tuple[int, int, int]] = []
        height = min(possible)
        if height > 4000000: break
        possible.remove(height)
        for line in parsed:
            dist = abs(line[0] - line[2]) + abs(line[1] - line[3])
            vdist = abs(line[1] - height)
            if dist >= vdist:
                delta = dist - vdist
                ranges.append((line[0] - delta, line[0] + delta + 1, -1 if height < line[1] else 1))
        ranges = list(sorted(ranges))
        ans = 0
        cur_last = 0
        for r in ranges:
            if r[0] > cur_last:
                result = cur_last * 4000000 + height
                cur_last = r[0]
            if r[1] <= cur_last:
                continue
            if r[1] > 4000000:
                ans += 4000000 - cur_last
                break
            ans += r[1] - cur_last
            cur_last = r[1]
        if ans != 4000000:
            good_h = height
            break
        filtered = list(filter(lambda x: x[2] == 1, ranges))
        for i in range(len(filtered)):
            for j in range(i + 1, len(filtered)):
                dist = (filtered[i][1] - filtered[j][0]) // 2 + 1
                if dist > 0:
                    possible.add(height + dist)
    submit(2, result)

if __name__ == "__main__":
    part1()
    part2()
