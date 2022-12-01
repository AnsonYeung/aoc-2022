#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from math import *

data = stdin.read().split('\n')[:-1]

def count():
    counts = []
    cur = 0
    for x in data:
        if x == "":
            counts.append(cur)
            cur = 0
        else:
            cur += int(x)
    counts.append(cur)
    return counts

def part1():
    counts = count()
    print(max(counts))

def part2():
    counts = list(sorted(count()))
    print(counts[-3] + counts[-2] + counts[-1])

if __name__ == "__main__":
    part1()
    part2()
