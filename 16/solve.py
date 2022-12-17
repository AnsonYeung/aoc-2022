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
    valve_dist = [[0 if i == j else 1 if i in adj[j] else len(valve_id) for i in range(len(valve_id))] for j in range(len(valve_id))]
    for i in range(len(valve_id)):
        for j in range(len(valve_id)):
            for k in range(len(valve_id)):
                if valve_dist[j][i] + valve_dist[i][k] < valve_dist[j][k]:
                    valve_dist[j][k] = valve_dist[j][i] + valve_dist[i][k]

def part1():
    ans = 0
    dp = [[[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(sp_valve) + 1)] for _ in range(31)]
    back_map: 'dict[int, int]' = {}
    back_map[len(sp_valve)] = valve_id["AA"]
    for oid in sp_valve_id:
        back_map[sp_valve_id[oid]] = oid
    dp[30][len(sp_valve)][0] = 0
    for timeLeft in range(30, 0, -1):
        for sid, valve in enumerate(dp[timeLeft]):
            for state, val in enumerate(valve):
                if val != -1:
                    for i in range(15):
                        if state & (1 << i): continue
                        d = valve_dist[back_map[sid]][back_map[i]]
                        new_time = timeLeft - d - 1
                        if new_time > 0:
                            dp[new_time][i][state | (1 << i)] = max(dp[new_time][i][state | (1 << i)], val + new_time * sp_valve[i])
                            if val + new_time * sp_valve[i] > ans:
                                ans = val + new_time * sp_valve[i]
    submit(1, ans)

def part2():
    ans = 0
    dp = [[[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(sp_valve) + 1)] for _ in range(27)]
    back_map: 'dict[int, int]' = {}
    back_map[len(sp_valve)] = valve_id["AA"]
    for oid in sp_valve_id:
        back_map[sp_valve_id[oid]] = oid
    dp[26][len(sp_valve)][0] = 0
    final_states: 'dict[int, int]' = {}
    for timeLeft in range(26, 0, -1):
        for sid, valve in enumerate(dp[timeLeft]):
            for state, val in enumerate(valve):
                if val != -1:
                    have_child = False
                    for i in range(15):
                        if state & (1 << i): continue
                        d = valve_dist[back_map[sid]][back_map[i]]
                        new_time = timeLeft - d - 1
                        if new_time > 0:
                            have_child = True
                            dp[new_time][i][state | (1 << i)] = max(dp[new_time][i][state | (1 << i)], val + new_time * sp_valve[i])
                            if val + new_time * sp_valve[i] > ans:
                                ans = val + new_time * sp_valve[i]
                    if not have_child:
                        if state not in final_states:
                            final_states[state] = val
                        if val > final_states[state]:
                            final_states[state] = val
    dp = [[[-1 for _ in range(2 ** len(sp_valve))] for _ in range(len(sp_valve) + 1)] for _ in range(27)]
    for state in final_states:
        dp[26][len(sp_valve)][state] = final_states[state]
    for timeLeft in range(26, 0, -1):
        for sid, valve in enumerate(dp[timeLeft]):
            for state, val in enumerate(valve):
                if val != -1:
                    for i in range(15):
                        if state & (1 << i): continue
                        d = valve_dist[back_map[sid]][back_map[i]]
                        new_time = timeLeft - d - 1
                        if new_time > 0:
                            dp[new_time][i][state | (1 << i)] = max(dp[new_time][i][state | (1 << i)], val + new_time * sp_valve[i])
                            if val + new_time * sp_valve[i] > ans:
                                ans = val + new_time * sp_valve[i]
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
