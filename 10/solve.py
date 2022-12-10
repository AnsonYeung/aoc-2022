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

def part1():
    ans = 0
    regX = 1
    hist: list[int] = []
    for insr in data:
        if insr == "noop":
            hist.append(regX)
            continue
        hist.append(regX)
        hist.append(regX)
        regX += int(insr.split(" ")[1])
    ans = sum(hist[i] * (i + 1) for i in range(19, 220, 40))
    submit(1, ans)

def part2():
    ans = 0
    regX = 1
    hist: list[int] = []
    for insr in data:
        if insr == "noop":
            hist.append(regX)
            continue
        hist.append(regX)
        hist.append(regX)
        regX += int(insr.split(" ")[1])
    cur_row = ""
    for i, pix in enumerate(hist):
        if abs(pix - i % 40) <= 1:
            cur_row += "X"
        else:
            cur_row += "."
        if i % 40 == 39:
            print(cur_row)
            cur_row = ""
    submit(2, "PLPAFBCL")

if __name__ == "__main__":
    part1()
    part2()
