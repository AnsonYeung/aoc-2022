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
    map: list[list[int]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)
    for i, line in enumerate(data):
        heights: list[int] = []
        for j, cell in enumerate(line):
            if cell == 'E':
                heights.append(25)
                end = (i, j)
            elif cell == 'S':
                heights.append(0)
                start = (i, j)
            else:
                heights.append(ord(cell) - ord('a'))
        map.append(heights)
    steps = [[10000000 for _ in line] for line in map]
    cur: list[tuple[int, int, int]] = [(start[0], start[1], 0)]
    while True:
        c = cur[0]
        cur = cur[1:]
        if c[2] >= steps[c[0]][c[1]]: continue
        steps[c[0]][c[1]] = c[2]
        if c[0] == end[0] and c[1] == end[1]:
            ans = c[2]
            submit(1, ans)
            return
        if c[0] > 0 and map[c[0] - 1][c[1]] - 1 <= map[c[0]][c[1]]:
            cur.append((c[0] - 1, c[1], c[2] + 1))
        if c[0] < len(map) - 1 and map[c[0] + 1][c[1]] - 1 <= map[c[0]][c[1]]:
            cur.append((c[0] + 1, c[1], c[2] + 1))
        if c[1] > 0 and map[c[0]][c[1] - 1] - 1 <= map[c[0]][c[1]]:
            cur.append((c[0], c[1] - 1, c[2] + 1))
        if c[1] < len(map[0]) - 1 and map[c[0]][c[1] + 1] - 1 <= map[c[0]][c[1]]:
            cur.append((c[0], c[1] + 1, c[2] + 1))

def part2():
    map: list[list[int]] = []
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)
    for i, line in enumerate(data):
        heights: list[int] = []
        for j, cell in enumerate(line):
            if cell == 'E':
                heights.append(25)
                end = (i, j)
            elif cell == 'S':
                heights.append(0)
                start = (i, j)
            else:
                heights.append(ord(cell) - ord('a'))
        map.append(heights)
    steps = [[10000000 for _ in line] for line in map]
    cur: list[tuple[int, int, int]] = [(end[0], end[1], 0)]
    while True:
        c = cur[0]
        cur = cur[1:]
        if c[2] >= steps[c[0]][c[1]]: continue
        steps[c[0]][c[1]] = c[2]
        if map[c[0]][c[1]] == 0:
            ans = c[2]
            submit(2, ans)
            return
        if c[0] > 0 and map[c[0] - 1][c[1]] + 1 >= map[c[0]][c[1]]:
            cur.append((c[0] - 1, c[1], c[2] + 1))
        if c[0] < len(map) - 1 and map[c[0] + 1][c[1]] + 1 >= map[c[0]][c[1]]:
            cur.append((c[0] + 1, c[1], c[2] + 1))
        if c[1] > 0 and map[c[0]][c[1] - 1] + 1 >= map[c[0]][c[1]]:
            cur.append((c[0], c[1] - 1, c[2] + 1))
        if c[1] < len(map[0]) - 1 and map[c[0]][c[1] + 1] + 1 >= map[c[0]][c[1]]:
            cur.append((c[0], c[1] + 1, c[2] + 1))

if __name__ == "__main__":
    part1()
    part2()
