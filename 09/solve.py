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
    cur = (0, 0)
    tail = (0, 0)
    tvisited: set[tuple[int, int]] = {tail}
    for line in data:
        x = line.split(' ')
        if x[0] == 'L': dir = (-1, 0)
        elif x[0] == 'R': dir = (1, 0)
        elif x[0] == 'D': dir = (0, -1)
        else: dir = (0, 1)
        for i in range(int(x[1])):
            cur = tuple(x + y for x, y in zip(cur, dir))
            if abs(tail[1] - cur[1]) > 1 and tail[0] == cur[0]:
                tail = (tail[0], tail[1] + (cur[1] - tail[1]) // abs(cur[1] - tail[1]))
            elif abs(tail[0] - cur[0]) > 1 and tail[1] == cur[1]:
                tail = (tail[0] + (cur[0] - tail[0]) // abs(cur[0] - tail[0]), tail[1])
            elif abs(tail[0] - cur[0]) > 1 or abs(tail[1] - cur[1]) > 1:
                tail = (tail[0] + (cur[0] - tail[0]) // abs(cur[0] - tail[0]), tail[1] + (cur[1] - tail[1]) // abs(cur[1] - tail[1]))
            tvisited.add(tail)
    submit(1, len(tvisited))

def part2():
    head = (0, 0)
    tails: list[tuple[int, int]] = [(0, 0) for i in range(9)]
    tvisited: set[tuple[int, int]] = {tails[8]}
    for line in data:
        x = line.split(' ')
        if x[0] == 'L': dir = (-1, 0)
        elif x[0] == 'R': dir = (1, 0)
        elif x[0] == 'D': dir = (0, -1)
        else: dir = (0, 1)
        for i in range(int(x[1])):
            head = tuple(x + y for x, y in zip(head, dir))
            cur = head
            for i, tail in enumerate(tails):
                if abs(tail[1] - cur[1]) > 1 and tail[0] == cur[0]:
                    tails[i] = (tail[0], tail[1] + (cur[1] - tail[1]) // abs(cur[1] - tail[1]))
                elif abs(tail[0] - cur[0]) > 1 and tail[1] == cur[1]:
                    tails[i] = (tail[0] + (cur[0] - tail[0]) // abs(cur[0] - tail[0]), tail[1])
                elif abs(tail[0] - cur[0]) > 1 or abs(tail[1] - cur[1]) > 1:
                    tails[i] = (tail[0] + (cur[0] - tail[0]) // abs(cur[0] - tail[0]), tail[1] + (cur[1] - tail[1]) // abs(cur[1] - tail[1]))
                cur = tail
            tvisited.add(tails[8])
    submit(2, len(tvisited))


if __name__ == "__main__":
    part1()
    part2()
