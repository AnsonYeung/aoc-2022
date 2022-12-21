#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
from tqdm import tqdm
from z3 import *
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
    parsed = {}
    for line in data:
        res = line.split(": ")
        if "0" <= res[1][0] <= "9":
            parsed[res[0]] = int(res[1])
        else:
            parsed[res[0]] = res[1].split(" ")

    parsed2 = {}
    for line in data:
        res = line.split(": ")
        if res[0] == "humn":
            parsed2[res[0]] = Int("x")
        elif "0" <= res[1][0] <= "9":
            parsed2[res[0]] = IntVal(int(res[1]))
        else:
            parsed2[res[0]] = res[1].split(" ")

def dfs(name: str):
    if type(parsed[name]) == int:
        return parsed[name]
    lhs = dfs(parsed[name][0])
    rhs = dfs(parsed[name][2])
    if parsed[name][1] == "+": result = lhs + rhs
    elif parsed[name][1] == "-": result = lhs - rhs
    elif parsed[name][1] == "*": result = lhs * rhs
    elif parsed[name][1] == "/": result = lhs // rhs
    else: assert False
    return result

def part1():
    ans = dfs("root")
    submit(1, ans)

def dfs2(name: str):
    if type(parsed2[name]) == list:
        lhs = dfs2(parsed2[name][0])
        rhs = dfs2(parsed2[name][2])
        if parsed2[name][1] == "+": result = lhs + rhs
        elif parsed2[name][1] == "-": result = lhs - rhs
        elif parsed2[name][1] == "*": result = lhs * rhs
        elif parsed2[name][1] == "/": result = lhs / rhs
        else: assert False
        parsed2[name] = result
    return parsed2[name]

def part2():
    lhs = dfs2(parsed2["root"][0])
    rhs = dfs2(parsed2["root"][2])
    s = Solver()
    s.add(lhs == rhs)
    assert(s.check())
    print(s.model())
    ans = s.model()[Int("x")]
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
