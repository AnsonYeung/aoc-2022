#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
from tqdm import tqdm
import re
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
    main = re.search(r"(?s)<main>(.*)</main>", res)
    if main:
        print(main.group(1))
    else:
        print(res)

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
    parsed = []
    for line in data:
        dval = 1
        val = 0
        for digit in reversed(line):
            if "0" <= digit <= "2":
                val += dval * int(digit)
            elif digit == "-":
                val -= dval
            elif digit == "=":
                val -= dval * 2
            dval *= 5
        parsed.append(val)

def part1():
    ans = sum(parsed)
    p1 = []
    while ans > 0:
        p1.append(ans % 5)
        ans //= 5
    delta = 0
    for i in range(len(p1)):
        p1[i] += delta
        delta = 0
        if p1[i] > 2:
            p1[i] -= 5
            delta = 1
        elif p1[i] < -2:
            p1[i] += 5
            delta = -1
    if delta != 0:
        p1.append(delta)
    submit(1, "".join("=" if x == -2 else "-" if x == -1 else str(x) for x in reversed(p1)))

def part2():
    ans = 0
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
