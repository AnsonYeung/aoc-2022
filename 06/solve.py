#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from math import *
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from init import get_session

def submit(part: int, ans):
    print(f"Submit answer {ans}")
    day = int(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
    r = requests.post(f"https://adventofcode.com/2022/day/{day}/answer", data={"level": part, "answer": ans}, cookies={"session": get_session()})
    print(r.text)

data = stdin.read().split('\n')[:-1]

def part1():
    counts = defaultdict(lambda: 0)
    cur_num = 0
    line = data[0]
    result = None
    for i in range(len(line)):
        if i >= 4:
            counts[line[i - 4]] -= 1
            if counts[line[i - 4]] == 0:
                cur_num -= 1
        if counts[line[i]] == 0:
            cur_num += 1
        counts[line[i]] += 1
        if cur_num == 4:
            result = i + 1
            break
    print(result)

def part2():
    counts = defaultdict(lambda: 0)
    cur_num = 0
    line = data[0]
    result = None
    for i in range(len(line)):
        if i >= 14:
            counts[line[i - 14]] -= 1
            if counts[line[i - 14]] == 0:
                cur_num -= 1
        if counts[line[i]] == 0:
            cur_num += 1
        counts[line[i]] += 1
        if cur_num == 14:
            result = i + 1
            break
    print(result)
    submit(2, result)

if __name__ == "__main__":
    part1()
    part2()
