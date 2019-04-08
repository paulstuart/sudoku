#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
import sys

class sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
    
    def col(self, x):
        return [row[x] for row in self.puzzle if row[x] != ' ']

    def row(self, x):
        return [n for n in self.puzzle[x] if n != ' ']
        return self.puzzle[x]

    def square(self, col, row):
        x = (col / 3) * 3
        y = (row / 3) * 3
        return [n for cols in self.puzzle[y:y+3] for n in cols[x:x+3] if n != ' ']

    def get(self, col, row):
        n = self.puzzle[row][col]
        return 0 if n==' ' else n

    def set(self, col, row, n):
        self.puzzle[row][col] = n

    def show(self):
        for row in self.puzzle:
            print(" ".join([str(x) for x in row]))

    def conflict(self, col, row, value):
        """conflict assumes that the value has not been applied (no self conflict)"""
        return ((value in self.col(col))  or
                (value in self.row(row))  or
                (value in self.square(col, row)))

    def duped(self, x, y, value):
        """differs from conflict in that cells are already applied"""
        for i, col in enumerate(self.puzzle[y]):
		if col == value and i != x:
			return True

        for i, row in enumerate(self.puzzle):
		if row[x] == value and i != y:
			return True

        # ugly but it works
        x2 = (x / 3) * 3
        y2 = (y / 3) * 3
        for i, row in enumerate(self.puzzle[y2:y2+3], y2):
            for j, col in enumerate(row[x2:x2+3], x2):
                if col == value and not (i == y and x == j):
                    return True

        return False

    def count(self):
        n = 0
        for row in self.puzzle:
            for col in row:
                if col != ' ' and col > 0:
                    n += 1
        return n

    def valid(self):
        for y, row in enumerate(self.puzzle):
            for x, n in enumerate(row):
                if self.duped(x, y, n):
                    return x, y
	return -1, -1


def solve(so, col, row):
    """solve a cell at a time and recursively guess new entries"""
    if col > 8:
        col = 0
        row += 1
        if row > 8:
            # done, no more recursion
            return so, True
    
    # already set?
    if so.get(col, row) > 0:
        # move on to next cell
        return solve(so, col+1, row)
    
    for n in random():
        if not so.conflict(col, row, n):
            so.set(col, row, n)
            solved, ok = solve(so, col+1, row)
            if ok:
                return solved, True

    # this is a dead end, retry up the call stack
    so.set(col, row, ' ')
    return so, False


def random():
    list = range(1,10)
    #shuffle(list)
    for i in list:
        yield i


def num(s):
    try:
        return int(s)
    except:
        return ' '


def load(filename):
    with open(filename) as f:
        puzzle = []
        for line in f:
            bits = [num(x) for x in line.split()]
            if len(bits) == 9:
                puzzle.append(bits)
        return sudoku(puzzle)


def main():
    try:
        filename = sys.argv[1]
    except:
        filename = 'sample.txt'

    so = load(filename)
    print("\ngiven ({}/81):".format(so.count()))
    so.show()

    solved, ok = solve(so, 0, 0)

    print("\nSOLVED: {}".format(ok))
    solved.show()
    print

    x, y = so.valid()
    if x >= 0 or y >= 0:
        print("invalid cell: {}, {}\n".format(x, y))

if __name__ == "__main__":
    main()


