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
    parsed = [list(map(int, x.split(","))) for x in data]
    cubes: 'set[tuple[int, int, int]]' = set(tuple(x) for x in parsed)

def part1():
    ans = 0
    for cube in cubes:
        if (cube[0] + 1, cube[1], cube[2]) not in cubes: ans += 1
        if (cube[0] - 1, cube[1], cube[2]) not in cubes: ans += 1
        if (cube[0], cube[1] + 1, cube[2]) not in cubes: ans += 1
        if (cube[0], cube[1] - 1, cube[2]) not in cubes: ans += 1
        if (cube[0], cube[1], cube[2] + 1) not in cubes: ans += 1
        if (cube[0], cube[1], cube[2] - 1) not in cubes: ans += 1
    submit(1, ans)

def part2():
    ans = 0
    outside: 'set[tuple[int, int, int]]' = {(0, 0, 0)}
    pending: 'list[tuple[int, int, int]]' = [(0, 0, 0)]
    legal = lambda x: -1 <= x[0] < 100 and -1 <= x[1] < 100 and -1 <= x[2] < 100 and x not in cubes
    while len(pending) > 0:
        cube = pending[-1]
        pending.pop()
        if (cube[0] + 1, cube[1], cube[2]) not in outside and legal((cube[0] + 1, cube[1], cube[2])):
            outside.add((cube[0] + 1, cube[1], cube[2]))
            pending.append((cube[0] + 1, cube[1], cube[2]))
        if (cube[0] - 1, cube[1], cube[2]) not in outside and legal((cube[0] - 1, cube[1], cube[2])):
            outside.add((cube[0] - 1, cube[1], cube[2]))
            pending.append((cube[0] - 1, cube[1], cube[2]))
        if (cube[0], cube[1] + 1, cube[2]) not in outside and legal((cube[0], cube[1] + 1, cube[2])):
            outside.add((cube[0], cube[1] + 1, cube[2]))
            pending.append((cube[0], cube[1] + 1, cube[2]))
        if (cube[0], cube[1] - 1, cube[2]) not in outside and legal((cube[0], cube[1] - 1, cube[2])):
            outside.add((cube[0], cube[1] - 1, cube[2]))
            pending.append((cube[0], cube[1] - 1, cube[2]))
        if (cube[0], cube[1], cube[2] + 1) not in outside and legal((cube[0], cube[1], cube[2] + 1)):
            outside.add((cube[0], cube[1], cube[2] + 1))
            pending.append((cube[0], cube[1], cube[2] + 1))
        if (cube[0], cube[1], cube[2] - 1) not in outside and legal((cube[0], cube[1], cube[2] - 1)):
            outside.add((cube[0], cube[1], cube[2] - 1))
            pending.append((cube[0], cube[1], cube[2] - 1))

    for cube in cubes:
        if (cube[0] + 1, cube[1], cube[2]) not in cubes and (cube[0] + 1, cube[1], cube[2]) in outside: ans += 1
        if (cube[0] - 1, cube[1], cube[2]) not in cubes and (cube[0] - 1, cube[1], cube[2]) in outside: ans += 1
        if (cube[0], cube[1] + 1, cube[2]) not in cubes and (cube[0], cube[1] + 1, cube[2]) in outside: ans += 1
        if (cube[0], cube[1] - 1, cube[2]) not in cubes and (cube[0], cube[1] - 1, cube[2]) in outside: ans += 1
        if (cube[0], cube[1], cube[2] + 1) not in cubes and (cube[0], cube[1], cube[2] + 1) in outside: ans += 1
        if (cube[0], cube[1], cube[2] - 1) not in cubes and (cube[0], cube[1], cube[2] - 1) in outside: ans += 1
    submit(2, ans)

if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    part1()
    part2()
