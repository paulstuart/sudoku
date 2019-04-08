#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
import sys

"""puzzle is a list of lists, e.g. puzzle[row][col], effectively y,x not x,y"""

def getcol(puzzle, x):
    return [row[x] for row in puzzle if row[x] > 0]

def getrow(puzzle, x):
    return [n for n in puzzle[x] if n > 0]

def square(puzzle, col, row):
    x = (col / 3) * 3
    y = (row / 3) * 3
    return [n for cols in puzzle[y:y+3] for n in cols[x:x+3] if n > 0]

def show(puzzle):
    for row in puzzle:
        print(" ".join([str(x) if x > 0 else " " for x in row]))

def conflict(puzzle, col, row, value):
    """conflict assumes that the value has not been applied (no puzzle conflict)"""
    return ((value in getcol(puzzle, col))  or
            (value in getrow(puzzle, row))  or
            (value in square(puzzle, col, row)))

def duped(puzzle, x, y, value):
    """differs from conflict in that cells are already applied"""

    # does value exist elsewhere in column x?
    for i, row in enumerate(puzzle):
        if row[x] == value and i != y:
            return True

    # does value exist elsewhere in row y?
    for i, col in enumerate(puzzle[y]):
        if col == value and i != x:
            return True

    # our smaller square
    x2 = (x / 3) * 3
    y2 = (y / 3) * 3
    for i, row in enumerate(puzzle[y2:y2+3], y2):
        for j, col in enumerate(row[x2:x2+3], x2):
            if col == value and not (i == y and x == j):
                return True

    return False

def count(puzzle):
    return sum([x > 0 for row in puzzle for x in row])

def valid(puzzle):
    for y, row in enumerate(puzzle):
        for x, n in enumerate(row):
            if n > 0:
                if duped(puzzle, x, y, n):
                    return x, y
    return -1, -1


def solve(puzzle, col, row):
    """solve a cell at a time and recursively guess new entries"""
    if col > 8:
        col = 0
        row += 1
        if row > 8:
            # all cells filled, we're done
            return puzzle, True
    
    # already set?
    if puzzle[row][col] > 0:
        # move on to next cell
        return solve(puzzle, col+1, row)
    
    for n in random():
        if not conflict(puzzle, col, row, n):
            puzzle[row][col] = n
            solved, ok = solve(puzzle, col+1, row)
            if ok:
                return solved, True

    # this is a dead end, retry up the call stack
    puzzle[row][col] = 0
    return puzzle, False


def random():
    list = range(1,10)
    #shuffle(list)
    for i in list:
        yield i


def num(s):
    try:
        return int(s)
    except:
        return 0


def load(filename):
    with open(filename) as f:
        puzzle = []
        for line in f:
            bits = [num(x) for x in line.split()]
            if len(bits) == 9:
                puzzle.append(bits)
        return puzzle


def main():
    try:
        filename = sys.argv[1]
    except:
        filename = 'sample.txt'

    puzzle = load(filename)
    print("\ngiven ({}/81):".format(count(puzzle)))
    show(puzzle)

    # make sure we can solve it!
    x, y = valid(puzzle)
    if x >= 0 or y >= 0:
        print("\ninvalid cell: {}, {}\n".format(x, y))
        sys.exit()

    solved, ok = solve(puzzle, 0, 0)

    print("\nSOLVED: {}".format(ok))
    show(solved)
    print

    x, y = valid(solved)
    if x >= 0 or y >= 0:
        print("invalid cell: {}, {}\n".format(x, y))

if __name__ == "__main__":
    main()

