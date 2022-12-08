#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from init import get_session

def submit(part: int, ans):
    res = input(f"Submit answer {ans}? [Y/n]")
    if 'N' in res or 'n' in res: return
    day = int(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
    r = requests.post(f"https://adventofcode.com/2022/day/{day}/answer", data={"level": part, "answer": ans}, cookies={"session": get_session()})
    print(r.text)

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]

def part1():
    ans = 0
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            for x in range(0, i):
                if data[x][j] >= val: break
            else:
                ans += 1
                continue
            for x in range(i + 1, len(data)):
                if data[x][j] >= val: break
            else:
                ans += 1
                continue
            for y in range(0, j):
                if data[i][y] >= val: break
            else:
                ans += 1
                continue
            for y in range(j + 1, len(line)):
                if data[i][y] >= val: break
            else:
                ans += 1
                continue
    submit(1, ans)

def part2():
    ans = 0
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            score = [0, 0, 0, 0]
            for x in range(i - 1, -1, -1):
                score[0] += 1
                if data[x][j] >= val:
                    break
            for x in range(i + 1, len(data)):
                score[1] += 1
                if data[x][j] >= val:
                    break
            for y in range(j - 1, -1, -1):
                score[2] += 1
                if data[i][y] >= val:
                    break
            for y in range(j + 1, len(line)):
                score[3] += 1
                if data[i][y] >= val:
                    break
            ans = max(ans, reduce(lambda x, y: x * y, score))
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
