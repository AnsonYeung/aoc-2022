#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from math import *

data = stdin.read().split('\n')[:-1]

def part1():
    score = 0
    for line in data:
        round = line.split(' ')
        opponent = ord(round[0]) - ord('A')
        me = ord(round[1]) - ord('X')
        result = (me - opponent) % 3
        if result == 0:
            score += 3
        elif result == 1:
            score += 6
        score += me + 1
    print(score)

def part2():
    score = 0
    for line in data:
        round = line.split(' ')
        opponent = ord(round[0]) - ord('A')
        me = (ord(round[1]) - ord('X') - 1 + opponent) % 3
        result = (me - opponent) % 3
        if result == 0:
            score += 3
        elif result == 1:
            score += 6
        score += me + 1
    print(score)

if __name__ == "__main__":
    part1()
    part2()
