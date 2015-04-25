#!/usr/bin/env python3
#
# Adapted from http://rosettacode.org/wiki/Maze_generation#Python

from random import shuffle, randrange
import sys

def make_maze(w = 16, h = 8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["# "] * w + ['#'] for _ in range(h)] + [[]]
    hor = [["##"] * w + ['#'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "# "
            if yy == y: ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    first = True
    i = len(ver) - 1
    print(str(w*2+1) + ',' + str(h*2+1))
    for (a, b) in zip(hor, ver):
        if first:
            b = ['#<'] + b[1:]
            first = False
        if i == 1:
            b = b[:-2] + [b[-2][0] + '>'] + [b[-1]]
        i -= 1
        print(''.join(a + ['\n'] + b))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        size = sys.argv[1].lower()
        if size == 'l':
            make_maze(30, 30)
        elif size == 'm':
            make_maze(20, 20)
        elif size == 's':
            make_maze()
    else:
        make_maze()
