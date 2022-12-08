#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
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
    ans = 0
    cur = []
    i = 0
    while i < len(data):
        assert(data[i][0] == '$')
        if data[i].startswith("$ cd "):
            if data[i] == "$ cd ..":
                sz = cur[-1]["size"]
                if sz < 100000:
                    ans += sz
                cur[-2]["size"] += sz
                cur.pop()
            else:
                cur.append({"name": data[i][5:], "size": 0})
            i += 1
        else:
            assert(data[i] == "$ ls")
            i += 1
            while i < len(data) and data[i][0] != '$':
                if data[i].startswith("dir "):
                    pass
                else:
                    cur[-1]["size"] += int(data[i].split(' ')[0])
                i += 1
    submit(1, ans)

def part2():
    ans = 0
    cur = []
    i = 0
    l = set()
    while i < len(data):
        assert(data[i][0] == '$')
        if data[i].startswith("$ cd "):
            if data[i] == "$ cd ..":
                sz = cur[-1]["size"]
                if sz < 100000:
                    ans += sz
                cur[-2]["size"] += sz
                assert(not l.add((cur[-1]["size"], cur[-1]["name"])))
                cur.pop()
            else:
                cur.append({"name": data[i][5:], "size": 0})
            i += 1
        else:
            assert(data[i] == "$ ls")
            i += 1
            while i < len(data) and data[i][0] != '$':
                if data[i].startswith("dir "):
                    pass
                else:
                    cur[-1]["size"] += int(data[i].split(' ')[0])
                i += 1
    need = cur[0]["size"] + cur[1]["size"] - 40000000
    print(cur)
    for x in sorted(l):
        if x[0] >= need:
            ans = x[0]
            print(x)
            break
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
