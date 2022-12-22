#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
from typing import Literal
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
    map = data[:-2]
    map_w = max(len(x) for x in map)
    map = list(x.ljust(map_w, " ") for x in map)
    action: 'list[Literal["L", "R"] | int]' = []
    num = 0
    for x in data[-1]:
        if x == "L" or x == "R":
            action.append(num)
            num = 0
            action.append(x)
        else:
            num = num * 10 + int(x)
    action.append(num)
    num = 0

    initial_x = 0
    while map[0][initial_x] == " ": initial_x += 1

def part1():
    loc_r = 0
    loc_c = initial_x
    dir = 0
    for x in action:
        if x == "L":
            dir = (dir - 1) % 4
        elif x == "R":
            dir = (dir + 1) % 4
        else:
            for _ in range(x):
                if dir == 0:
                    orig = loc_c
                    loc_c = (loc_c + 1) % map_w
                    while map[loc_r][loc_c] == " ":
                        loc_c = (loc_c + 1) % map_w
                    if map[loc_r][loc_c] == "#":
                        loc_c = orig
                elif dir == 2:
                    orig = loc_c
                    loc_c = (loc_c - 1) % map_w
                    while map[loc_r][loc_c] == " ":
                        loc_c = (loc_c - 1) % map_w
                    if map[loc_r][loc_c] == "#":
                        loc_c = orig
                elif dir == 1:
                    orig = loc_r
                    loc_r = (loc_r + 1) % len(map)
                    while map[loc_r][loc_c] == " ":
                        loc_r = (loc_r + 1) % len(map)
                    if map[loc_r][loc_c] == "#":
                        loc_r = orig
                elif dir == 3:
                    orig = loc_r
                    loc_r = (loc_r - 1) % len(map)
                    while map[loc_r][loc_c] == " ":
                        loc_r = (loc_r - 1) % len(map)
                    if map[loc_r][loc_c] == "#":
                        loc_r = orig
    ans = 4 * (loc_c + 1) + 1000 * (loc_r + 1) + dir
    submit(1, ans)

def part2():
    loc_r = 0
    loc_c = initial_x
    dir = 0
    edge_map: 'dict[tuple[int, int, int], tuple[int, int, int]]' = {}
    for i in range(50):
        def link(pos1: 'tuple[int, int]', dir1: int, pos2: 'tuple[int, int]', dir2: int):
            edge_map[(*pos1, dir1)] = (*pos2, (dir2 + 2) % 4)
            edge_map[(*pos2, dir2)] = (*pos1, (dir1 + 2) % 4)
        link((0, 50 + i), 3, (150 + i, 0), 2)
        link((0, 100 + i), 3, (199, i), 1)
        link((i, 50), 2, (149 - i, 0), 2)
        link((i, 149), 0, (149 - i, 99), 0)
        link((50 + i, 50), 2, (100, i), 3)
        link((50 + i, 99), 0, (49, 100 + i), 1)
        link((149, 50 + i), 1, (150 + i, 49), 0)
    for x in action:
        if x == "L":
            dir = (dir - 1) % 4
        elif x == "R":
            dir = (dir + 1) % 4
        else:
            for _ in range(x):
                if dir == 0:
                    orig = loc_r, loc_c, dir
                    loc_c += 1
                    if not 0 <= loc_c < map_w or map[loc_r][loc_c] == " ":
                        loc_r, loc_c, dir = edge_map[orig]
                    if map[loc_r][loc_c] == "#":
                        loc_r, loc_c, dir = orig
                elif dir == 2:
                    orig = loc_r, loc_c, dir
                    loc_c -= 1
                    if not 0 <= loc_c < map_w or map[loc_r][loc_c] == " ":
                        loc_r, loc_c, dir = edge_map[orig]
                    if map[loc_r][loc_c] == "#":
                        loc_r, loc_c, dir = orig
                elif dir == 1:
                    orig = loc_r, loc_c, dir
                    loc_r += 1
                    if not 0 <= loc_r < len(map) or map[loc_r][loc_c] == " ":
                        loc_r, loc_c, dir = edge_map[orig]
                    if map[loc_r][loc_c] == "#":
                        loc_r, loc_c, dir = orig
                elif dir == 3:
                    orig = loc_r, loc_c, dir
                    loc_r -= 1
                    if not 0 <= loc_r < len(map) or map[loc_r][loc_c] == " ":
                        loc_r, loc_c, dir = edge_map[orig]
                    if map[loc_r][loc_c] == "#":
                        loc_r, loc_c, dir = orig
    ans = 4 * (loc_c + 1) + 1000 * (loc_r + 1) + dir
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
