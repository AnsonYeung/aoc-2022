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
    print(res)
    main = re.search(r"<main>([.\n]*)</main>", res)
    if main:
        print(main.group(1))
    else:
        print(res.split("\n")[-16])

with open("input.txt", "r") as f:
    data = list(map(int, f.read().split('\n')[:-1]))
    # data = [1, 2, -3, 3, -2, 0, 4]

def part1():
    arr = list(enumerate(data))
    for i in range(len(data)):
        loc = 0
        while arr[loc][0] != i:
            loc += 1
        to_move = arr[loc][1] % (len(arr) - 1)
        for _ in range(to_move):
            tmp = arr[loc]
            arr[loc] = arr[(loc + 1) % len(arr)]
            arr[(loc + 1) % len(arr)] = tmp
            loc = (loc + 1) % len(arr)
    zero_pos = 0
    while arr[zero_pos][1] != 0:
        zero_pos += 1
    ans = sum(arr[(zero_pos + 1000 * i) % len(arr)][1] for i in range(1, 4))
    submit(1, ans)

def part2():
    arr = list((i, x * 811589153) for i, x in enumerate(data))
    for _ in range(10):
        for i in range(len(data)):
            loc = 0
            while arr[loc][0] != i:
                loc += 1
            to_move = arr[loc][1] % (len(arr) - 1)
            for _ in range(to_move):
                tmp = arr[loc]
                arr[loc] = arr[(loc + 1) % len(arr)]
                arr[(loc + 1) % len(arr)] = tmp
                loc = (loc + 1) % len(arr)
    zero_pos = 0
    while arr[zero_pos][1] != 0:
        zero_pos += 1
    ans = sum(arr[(zero_pos + 1000 * i) % len(arr)][1] for i in range(1, 4))
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
