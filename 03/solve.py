#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from math import *

data = stdin.read().split('\n')[:-1]

def prio(y):
    if 'a' <= y <= 'z':
        return ord(y) - ord('a') + 1
    else:
        return ord(y) - ord('A') + 1 + 26

def part1():
    count = 0
    for x in data:
        first = set(x[:len(x)//2])
        second = set(x[len(x)//2:])
        assert len(x) % 2 == 0
        for y in first:
            if y in second:
                count += prio(y)
                break
    print(count)

def part2():
    count = 0
    for i in range(0, len(data), 3):
        first = set(data[i])
        second = set(data[i + 1])
        third = set(data[i + 2])
        for x in first:
            if x in second and x in third:
                count += prio(x)
                break
    print(count)

if __name__ == "__main__":
    part1()
    part2()
