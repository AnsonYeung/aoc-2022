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
    items: list[list[int]] = []
    ops: list[tuple[int, str, int]] = []
    act: list[list[int]] = []
    for i in range(0, len(data), 7):
        items.append(list(map(int, data[i + 1].split(": ")[1].split(", "))))
        command = data[i + 2].split("= ")[1].split(" ")
        ops.append((0 if command[0] == "old" else int(command[0]), command[1], 0 if command[2] == "old" else int(command[2])))
        div = int(data[i + 3].split("by ")[1])
        tm = int(data[i + 4].split("monkey ")[1])
        fm = int(data[i + 5].split("monkey ")[1])
        act.append([div, tm, fm])
    
    counts: list[int] = [0] * len(items)
    base = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19
    for _ in range(20):
        for i, itemlist in enumerate(items):
            counts[i] += len(itemlist)
            for item in itemlist:
                if ops[i][1] == "+":
                    item = (ops[i][0] or item) + (ops[i][2] or item)
                else:
                    item = (ops[i][0] or item) * (ops[i][2] or item)
                item //=3
                if item % act[i][0] == 0:
                    items[act[i][1]].append(item % base)
                else:
                    items[act[i][2]].append(item % base)
            items[i] = []
    result = list(sorted(counts))
    ans = result[-1] * result[-2]
    submit(2, ans)

def part2():
    ans = 0
    items: list[list[int]] = []
    ops: list[tuple[int, str, int]] = []
    act: list[list[int]] = []
    for i in range(0, len(data), 7):
        items.append(list(map(int, data[i + 1].split(": ")[1].split(", "))))
        command = data[i + 2].split("= ")[1].split(" ")
        ops.append((0 if command[0] == "old" else int(command[0]), command[1], 0 if command[2] == "old" else int(command[2])))
        div = int(data[i + 3].split("by ")[1])
        tm = int(data[i + 4].split("monkey ")[1])
        fm = int(data[i + 5].split("monkey ")[1])
        act.append([div, tm, fm])
    
    counts: list[int] = [0] * len(items)
    base = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19
    for _ in range(10000):
        for i, itemlist in enumerate(items):
            counts[i] += len(itemlist)
            for item in itemlist:
                if ops[i][1] == "+":
                    item = (ops[i][0] or item) + (ops[i][2] or item)
                else:
                    item = (ops[i][0] or item) * (ops[i][2] or item)
                if item % act[i][0] == 0:
                    items[act[i][1]].append(item % base)
                else:
                    items[act[i][2]].append(item % base)
            items[i] = []
    result = list(sorted(counts))
    ans = result[-1] * result[-2]
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
