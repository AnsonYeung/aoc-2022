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
    print(res.split("\n")[-16])

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
    parsed: 'list[list[int]]' = []
    for line in data:
        res = re.match(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
        assert res is not None
        parsed.append(list(map(int, res.groups())))
    print(parsed)

def dfs(time_left: int, cur_state: 'list[int]', blueprint: 'list[int]', cache):
    k = tuple(cur_state + [time_left])
    if k in cache:
        return cache[k]

    # determine bad moves
    if cur_state[0] > blueprint[7] or cur_state[1] > blueprint[8] or cur_state[2] > blueprint[9]:
        return 0

    best = cur_state[3] * time_left + cur_state[7]

    t = -(-(blueprint[1] - cur_state[4]) // cur_state[0])
    if t < 0: t = 0
    if t + 1 < time_left:
        new_state = list(cur_state[i] if i < 4 else cur_state[i] + cur_state[i - 4] * (t + 1) for i in range(8))
        new_state[4] -= blueprint[1]
        new_state[0] += 1
        best = max(best, dfs(time_left - t - 1, new_state, blueprint, cache))

    t = -(-(blueprint[2] - cur_state[4]) // cur_state[0])
    if t < 0: t = 0
    if t + 1 < time_left:
        new_state = list(cur_state[i] if i < 4 else cur_state[i] + cur_state[i - 4] * (t + 1) for i in range(8))
        new_state[4] -= blueprint[2]
        new_state[1] += 1
        best = max(best, dfs(time_left - t - 1, new_state, blueprint, cache))
    
    if cur_state[1] != 0:
        t = max(-(-(blueprint[3] - cur_state[4]) // cur_state[0]), -(-(blueprint[4] - cur_state[5]) // cur_state[1]))
        if t < 0: t = 0
        if t + 1 < time_left:
            new_state = list(cur_state[i] if i < 4 else cur_state[i] + cur_state[i - 4] * (t + 1) for i in range(8))
            new_state[4] -= blueprint[3]
            new_state[5] -= blueprint[4]
            new_state[2] += 1
            best = max(best, dfs(time_left - t - 1, new_state, blueprint, cache))

    if cur_state[2] != 0:
        t = max(-(-(blueprint[5] - cur_state[4]) // cur_state[0]), -(-(blueprint[6] - cur_state[6]) // cur_state[2]))
        if t < 0: t = 0
        if t + 1 < time_left:
            new_state = list(cur_state[i] if i < 4 else cur_state[i] + cur_state[i - 4] * (t + 1) for i in range(8))
            new_state[4] -= blueprint[5]
            new_state[6] -= blueprint[6]
            new_state[3] += 1
            best = max(best, dfs(time_left - t - 1, new_state, blueprint, cache))

    cache[k] = best
    return best

def add_state(states: 'set[tuple[int, int, int, int, int, int, int, int]]', state: 'list[int]'):
    states.add(tuple(state[i] if i < 4 else state[i - 4] + state[i] for i in range(8)))

def part1():
    ans = 0
    for blueprint in tqdm(parsed):
        blueprint = blueprint + [max(blueprint[1], blueprint[2], blueprint[3], blueprint[5]), blueprint[4], blueprint[6]]
        ans += blueprint[0] * dfs(24, [1, 0, 0, 0, 0, 0, 0, 0], blueprint, {})
    submit(1, ans)

def part2():
    ans = 1
    for i in tqdm(range(3)):
        blueprint = parsed[i]
        blueprint = blueprint + [max(blueprint[1], blueprint[2], blueprint[3], blueprint[5]), blueprint[4], blueprint[6]]
        ans *= dfs(32, [1, 0, 0, 0, 0, 0, 0, 0], blueprint, {})
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
