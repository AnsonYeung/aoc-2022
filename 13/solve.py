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
from init import get_session

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


def compare(x, y) -> int:
    if type(x) == int and type(y) == int:
        if x < y: return -1
        elif x == y: return 0
        else: return 1
    if type(x) == int:
        x = [x]
    if type(y) == int:
        y = [y]
    for i in range(min(len(x), len(y))):
        res = compare(x[i], y[i])
        if res == -1: return -1
        if res == 1: return 1
    if len(x) < len(y): return -1
    elif len(x) > len(y): return 1
    else: return 0


def part1():
    ans = 0
    for i in range(0, len(data), 3):
        x1 = eval(data[i])
        x2 = eval(data[i + 1])
        if compare(x1, x2) <= 0:
            ans += i // 3 + 1
    submit(1, ans)

def part2():
    packets = list(filter(lambda x: x != "", data))
    packets.append("[[2]]")
    packets.append("[[6]]")
    packets.sort(key=cmp_to_key(lambda x, y: compare(eval(x), eval(y))))
    idx1 = packets.index("[[2]]") + 1
    idx2 = packets.index("[[6]]") + 1
    submit(2, idx1 * idx2)

if __name__ == "__main__":
    part1()
    part2()
