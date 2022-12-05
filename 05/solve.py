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
    print(f"Submit answer {ans}")
    day = int(os.path.basename(os.path.dirname(__file__)))
    r = requests.post(f"https://adventofcode.com/2022/day/{day}/answer", data={"level": part, "answer": ans}, cookies={"session": get_session()})
    print(r.text)

data = stdin.read().split('\n')[:-1]

def part1():
    row = 0
    state = []
    while data[row] != "":
        cur = []
        for i in range(9):
            cur.append(data[row][i * 4 + 1])
        state.append(cur)
        row += 1
    state = state[:-1]
    cur_state = []
    for i in range(9):
        cur = []
        j = 7
        while j >= 0 and state[j][i] != ' ':
            cur.append(state[j][i])
            j -= 1
        cur_state.append(cur)

    row += 1
    while row < len(data):
        insr = data[row][5:]
        s1 = insr.split(' from ')
        num = int(s1[0])
        src = int(s1[1].split(' to ')[0]) - 1
        dst = int(s1[1].split(' to ')[1]) - 1
        for i in range(num):
            c = cur_state[src].pop()
            cur_state[dst].append(c)
        row += 1

    result = ""
    for i in range(9):
        result += cur_state[i][-1]
    print(result)

    # submit(1, ans)

def part2():
    row = 0
    state = []
    while data[row] != "":
        cur = []
        for i in range(9):
            cur.append(data[row][i * 4 + 1])
        state.append(cur)
        row += 1
    state = state[:-1]
    cur_state = []
    for i in range(9):
        cur = []
        j = 7
        while j >= 0 and state[j][i] != ' ':
            cur.append(state[j][i])
            j -= 1
        cur_state.append(cur)

    row += 1
    while row < len(data):
        insr = data[row][5:]
        s1 = insr.split(' from ')
        num = int(s1[0])
        src = int(s1[1].split(' to ')[0]) - 1
        dst = int(s1[1].split(' to ')[1]) - 1
        for x in cur_state[src][-num:]:
            cur_state[dst].append(x)
        cur_state[src] = cur_state[src][:-num]
        row += 1

    result = ""
    for i in range(9):
        result += cur_state[i][-1]
    print(result)


if __name__ == "__main__":
    part1()
    part2()
