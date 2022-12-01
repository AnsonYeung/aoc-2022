#!/usr/bin/env python3
import argparse
import os
import shutil
import requests
import logging
import time
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(
        description="Create a file using the template and download right when the problem start",
        )

parser.add_argument("day", type=int)
parser.add_argument("-t", "--template-file", default="template/default.py")
parser.add_argument("-y", "--year", default=2022, type=int)
parser.add_argument("-i", "--immediate", action="store_true", default=False)
parser.add_argument("--input-only", action="store_true", default=False)

if __name__ == "__main__":
    args = parser.parse_args()
    day_str = "%02d" % args.day
    
    if not args.input_only:
        os.makedirs(day_str)
        shutil.copyfile(args.template_file, f"{day_str}/solve.py")

    with open(".env/session", "r") as sessFile:
        session = sessFile.read().strip()

    if not args.immediate:
        cur = datetime.now()
        startTime = cur.replace(microsecond=0, second=0, minute=0) + timedelta(hours = 1)
        print(f"Starting time: {startTime}")
        print()
        while cur < startTime:
            cur = datetime.now()
            print(f"\rRemaining time: {(startTime - cur).seconds}s", end='')
            time.sleep(1)

    r = requests.get(f"https://adventofcode.com/{args.year}/day/{args.day}/input", cookies={"session": session})

    with open(f"{day_str}/input.txt", "w") as inpFile:
        inpFile.write(r.text)
