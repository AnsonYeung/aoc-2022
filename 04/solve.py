#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from math import *

data = stdin.read().split('\n')[:-1]

def part1():
    count = 0
    for x in data:
        splited = x.split(',')
        first = list(map(int, splited[0].split('-')))
        second = list(map(int, splited[1].split('-')))
        if first[0] <= second[0] and first[1] >= second[1]:
            count += 1
        elif first[0] >= second[0] and first[1] <= second[1]:
            count += 1
    print(count)

def part2():
    count = 0
    for x in data:
        splited = x.split(',')
        first = list(map(int, splited[0].split('-')))
        second = list(map(int, splited[1].split('-')))
        if first[0] <= second[1] and first[1] >= second[0]:
            count += 1
    print(count)

if __name__ == "__main__":
    part1()
    part2()
