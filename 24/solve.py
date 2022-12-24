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
    height = len(data) - 2
    width = len(data[0]) - 2
    period = height * width
    blizz = []
    for i, line in enumerate(data[1:-1]):
        for j, direction in enumerate(line[1:-1]):
            if direction == ">":
                blizz.append((i, j, 0, 1))
            elif direction == "<":
                blizz.append((i, j, 0, -1))
            elif direction == "v":
                blizz.append((i, j, 1, 0))
            elif direction == "^":
                blizz.append((i, j, -1, 0))
            else:
                assert direction == "."

def part1():
    def is_ok1(r, c, i):
        for b in blizz:
            if (b[1] + b[3] * i) % width == c and (b[0] + b[2] * i) % height == r:
                return False
        return True
    state = {(-1, 0, 0): 0}
    new_states = [(-1, 0, 0)]
    mx = 0
    while True:
        s = new_states[0]
        new_states = new_states[1:]
        found = False
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            new_pos = (s[0] + dir[0], s[1] + dir[1])
            if dir != (0, 0) and (not 0 <= new_pos[0] < height or not 0 <= new_pos[1] < width):
                continue
            if (*new_pos, (s[2] + 1) % period) in state:
                continue
            if not is_ok1(*new_pos, s[2] + 1):
                continue
            if new_pos == (height - 1, width - 1):
                ans = s[2] + 2
                found = True
                break
            state[(*new_pos, (s[2] + 1) % period)] = state[s] + 1
            new_states.append((*new_pos, (s[2] + 1) % period))
            if state[s] + 1 > mx:
                mx = state[s] + 1
        if found:
            break
    submit(1, ans)

def part2():
    def is_ok1(r, c, i):
        for b in blizz:
            if (b[1] + b[3] * i) % width == c and (b[0] + b[2] * i) % height == r:
                return False
        return True
    state = {(-1, 0, 0): 0}
    new_states = [(-1, 0, 0)]
    num = 0
    while True:
        s = new_states[0]
        new_states = new_states[1:]
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            new_pos = (s[0] + dir[0], s[1] + dir[1])
            if dir != (0, 0) and (not 0 <= new_pos[0] < height or not 0 <= new_pos[1] < width):
                continue
            if (*new_pos, (s[2] + 1) % period) in state:
                continue
            if not is_ok1(*new_pos, s[2] + 1):
                continue
            if new_pos == (height - 1, width - 1) and num % 2 == 0:
                num += 1
                print(num, s[2] + 2)
                ans = s[2] + 2
                state = {(height, width - 1, (s[2] + 2) % period): s[2] + 2}
                new_states = [(height, width - 1, (s[2] + 2) % period)]
                break
            if new_pos == (0, 0) and num % 2 == 1:
                num += 1
                print(num, s[2] + 2)
                ans = s[2] + 2
                state = {(-1, 0, (s[2] + 2) % period): s[2] + 2}
                new_states = [(-1, 0, (s[2] + 2) % period)]
                break
            state[(*new_pos, (s[2] + 1) % period)] = state[s] + 1
            new_states.append((*new_pos, (s[2] + 1) % period))
        if num == 3:
            break
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
