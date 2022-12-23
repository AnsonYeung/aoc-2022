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
    main = re.search(r"(?s)<main>(.*)</main>", res)
    if main:
        print(main.group(1))
    else:
        print(res)

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
#    data = """\
#..............
#..............
#.......#......
#.....###.#....
#...#...#.#....
#....#...##....
#...#.###......
#...##.#.##....
#....#..#......
#..............
#..............
#..............\
#""".split('\n')
    orig_pos: 'set[tuple[int, int]]' = set()
    for i, line in enumerate(data):
        for j, box in enumerate(line):
            if box == "#":
                orig_pos.add((i, j))

def part1():
    order = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elfs_pos = orig_pos
    num_elfs = len(elfs_pos)
    for _ in range(10):
        new_pos: 'dict[tuple[int, int], tuple[int, int]]' = {}
        collided_pos = set()
        for pos in elfs_pos:
            # check surround 8
            for i, j in product(range(-1, 2), repeat=2):
                if (i != 0 or j != 0) and (pos[0] + i, pos[1] + j) in elfs_pos:
                    break
            else:
                new_pos[pos] = pos
                continue
            for o in order:
                o1 = (o[0] or -1, o[1] or -1)
                o2 = (o[0] or 1, o[1] or 1)
                if (pos[0] + o[0], pos[1] + o[1]) not in elfs_pos and (pos[0] + o1[0], pos[1] + o1[1]) not in elfs_pos and (pos[0] + o2[0], pos[1] + o2[1]) not in elfs_pos:
                    npos = (pos[0] + o[0], pos[1] + o[1])
                    if npos in new_pos:
                        collided_pos.add(npos)
                        new_pos[new_pos[npos]] = new_pos[npos]
                        new_pos[pos] = pos
                    else:
                        new_pos[npos] = pos
                    break
            else:
                new_pos[pos] = pos
        elfs_pos = set(new_pos.keys())
        for pos in collided_pos:
            elfs_pos.remove(pos)
        order = order[1:] + order[:1]
    assert num_elfs == len(elfs_pos)
    ans = (max(i for i, j in elfs_pos) - min(i for i, j in elfs_pos) + 1) * (max(j for i, j in elfs_pos) - min(j for i, j in elfs_pos) + 1) - num_elfs

    submit(1, ans)

def part2():
    order = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elfs_pos = orig_pos
    num_elfs = len(elfs_pos)
    cnt = 0
    moved = True
    while moved:
        moved = False
        new_pos: 'dict[tuple[int, int], tuple[int, int]]' = {}
        collided_pos = set()
        for pos in elfs_pos:
            # check surround 8
            for i, j in product(range(-1, 2), repeat=2):
                if (i != 0 or j != 0) and (pos[0] + i, pos[1] + j) in elfs_pos:
                    break
            else:
                new_pos[pos] = pos
                continue
            for o in order:
                o1 = (o[0] or -1, o[1] or -1)
                o2 = (o[0] or 1, o[1] or 1)
                if (pos[0] + o[0], pos[1] + o[1]) not in elfs_pos and (pos[0] + o1[0], pos[1] + o1[1]) not in elfs_pos and (pos[0] + o2[0], pos[1] + o2[1]) not in elfs_pos:
                    npos = (pos[0] + o[0], pos[1] + o[1])
                    if npos in new_pos:
                        collided_pos.add(npos)
                        new_pos[new_pos[npos]] = new_pos[npos]
                        new_pos[pos] = pos
                    else:
                        new_pos[npos] = pos
                    break
            else:
                new_pos[pos] = pos
        old_pos = elfs_pos
        elfs_pos = set(new_pos.keys())
        for pos in collided_pos:
            elfs_pos.remove(pos)
        order = order[1:] + order[:1]
        for pos in old_pos:
            if pos not in elfs_pos:
                moved = True
                break
        cnt += 1
    assert num_elfs == len(elfs_pos)
    ans = cnt
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
