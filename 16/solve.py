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
#     data = """
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II
# """.strip().split("\n")
    valve_id: 'dict[str, int]' = {}
    sp_valve: 'list[int]' = []
    sp_valve_id: 'dict[int, int]' = {}
    for i, line in enumerate(data):
        name = line[6:8]
        valve_id[name] = i
        result = re.search(r"=(\d+);", line)
        assert result is not None
        rate = int(result.group(1))
        if rate != 0:
            sp_valve_id[i] = len(sp_valve)
            sp_valve.append(rate)
    adj: 'list[list[int]]' = []
    for line in data:
        connected = line.split("to valve")[1][1:].strip().split(", ")
        adj.append([valve_id[x] for x in connected])
    inc: 'list[int]' = []
    for i in range(2 ** len(sp_valve)):
        total = 0
        for id, val in enumerate(sp_valve):
            if i & (1 << id):
                total += val
        inc.append(total)

def part1():
    dp: 'list[list[int]]' = [[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(valve_id))]
    dp[valve_id["AA"]][0] = 0
    for _ in range(30):
        new_dp: 'list[list[int]]' = [[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(valve_id))]
        for id, valve in enumerate(dp):
            for state, val in enumerate(valve):
                if val != -1:
                    if id in sp_valve_id:
                        new_state = state | (1 << sp_valve_id[id])
                        new_dp[id][new_state] = max(new_dp[id][new_state], val + inc[state])
                    for new_id in adj[id]:
                        new_dp[new_id][state] = max(new_dp[new_id][state], val + inc[state])
        dp = new_dp
    ans = max(max(x) for x in dp)
    submit(1, ans)

def part2():
    dp = [[[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(valve_id))] for _ in range(len(valve_id))]
    dp[valve_id["AA"]][valve_id["AA"]][0] = 0
    for _ in tqdm(range(26)):
        new_dp = [[[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(valve_id))] for _ in range(len(valve_id))]
        for id, x in enumerate(dp):
            for ele_id, valve in enumerate(x):
                for state, val in enumerate(valve):
                    if val != -1:
                        if ele_id in sp_valve_id:
                            s = state | (1 << sp_valve_id[ele_id])
                            if id in sp_valve_id:
                                new_state = s | (1 << sp_valve_id[id])
                                new_dp[id][ele_id][new_state] = max(new_dp[id][ele_id][new_state], val + inc[state])
                            for new_id in adj[id]:
                                new_dp[new_id][ele_id][s] = max(new_dp[new_id][ele_id][s], val + inc[state])
                        for new_ele_id in adj[ele_id]:
                            if id in sp_valve_id:
                                new_state = state | (1 << sp_valve_id[id])
                                new_dp[id][new_ele_id][new_state] = max(new_dp[id][new_ele_id][new_state], val + inc[state])
                            for new_id in adj[id]:
                                new_dp[new_id][new_ele_id][state] = max(new_dp[new_id][new_ele_id][state], val + inc[state])
        dp = new_dp
    ans = max(max(max(y) for y in x) for x in dp)
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
