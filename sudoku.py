#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
import sys

"""puzzle is a list of lists, e.g. puzzle[[row1][row2]...], effectively y,x not x,y"""

def show(puzzle):
    for row in puzzle:
        print(" ".join([str(x) if x > 0 else " " for x in row]))

def duped(puzzle, x, y, value):
    # does value exist elsewhere in column x?
    for i, row in enumerate(puzzle):
        if row[x] == value and i != y:
            return True

    # does value exist elsewhere in row y?
    for i, col in enumerate(puzzle[y]):
        if col == value and i != x:
            return True

    # our small square
    x2 = (x / 3) * 3
    y2 = (y / 3) * 3
    for i, row in enumerate(puzzle[y2:y2+3], y2):
        for j, col in enumerate(row[x2:x2+3], x2):
            if col == value and not (i == y and x == j):
                return True

    return False

def solve(puzzle, col, row):
    """solve one cell at a time and recursively guess new entries"""
    if col > 8:
        col = 0
        row += 1
        if row > 8:
            # all cells filled, we're done
            return puzzle, True
    
    # skip if already set
    if puzzle[row][col] > 0:
        return solve(puzzle, col+1, row)
    
    for n in random():
        if not duped(puzzle, col, row, n):
            puzzle[row][col] = n
            solved, ok = solve(puzzle, col+1, row)
            if ok:
                return solved, True

    # this is a dead end, retry up the call stack
    puzzle[row][col] = 0
    return puzzle, False

def random():
    list = range(1,10)
    shuffle(list)
    return list

def load(filename):
    with open(filename) as f:
        puzzle = []
        for line in f:
            bits = [num(x) for x in line.split()]
            if len(bits) == 9:
                puzzle.append(bits)
        return puzzle

def num(s):
    try:
        return int(s)
    except:
        return 0

def valid(puzzle):
    for y, row in enumerate(puzzle):
        for x, n in enumerate(row):
            if (n > 0 and duped(puzzle, x, y, n)):
                print("\nduplicate entry: {} @ {}, {}\n".format(n, x+1, y+1))
                sys.exit()

def count(puzzle):
    return sum([x > 0 for row in puzzle for x in row])


def main():
    try:
        filename = sys.argv[1]
    except:
        filename = 'sample.txt'

    puzzle = load(filename)
    print("\ngiven ({}/81):".format(count(puzzle)))
    show(puzzle)

    # make sure we can solve it!
    valid(puzzle)

    solved, ok = solve(puzzle, 0, 0)

    print("\nSOLVED: {}".format(ok))
    show(solved)
    print

    # prove that we actually solved it
    valid(puzzle)


if __name__ == "__main__":
    main()

