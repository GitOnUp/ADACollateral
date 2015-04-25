#!/usr/bin/env python3

# mazesolver.py
#
# Skeleton implementation of a maze solver.  Contains helpers to load mazes and
# determine if a move from one cell to another is legal (doesn't run into a wall
# or off of the board).  It also stores the start ('<') and end ('>') positions.
#
# There is a solve function, that currently only prints the characters in the
# maze.  Your goal is to start from the start character and draw a path of '.'
# characters in self.maze to the end character, then print it.  So for example:
#
# #########           #########
# #<#     #           #<#.....#
# # # ### #  becomes  #.#.###.#
# #     #>#           #...  #>#
# #########           #########
#
# Mazes can be generated by running the accompanying makeamaze.py and saving the
# output.  You can optionally pass L M or S to make large, medium or small mazes.
#
# On 4/21 we talked about how stacks can be used to perform a depth-first search;
# on 4/14 we talked about breadth-first searches in terms of word twisting, using
# a queue.
#
# Both of these approaches can be used to build a solution to a maze.
# There are further hints in hints.base64.  This file is obfuscated so you don't
# spoil any fun for yourselves.  To unlock it, from your terminal:
#
#   cat hints.base64 | base64 -d > hints.txt
#
# Then open hints.txt.
# m1.txt, m2.txt, and m3.txt are mazes that may help ferret out bugs.
import sys

class Maze(object):
    def __init__(self, filename):
        # this will be a 2d array, with self.maze[0] being the entire first row,
        # and self.maze[0][0] being the first character of that row (y,x coordinates).
        # because we read lines and add them to the maze, maze[1] is actually below
        # maze[0]: the y axis is inverted compared to how you normally think about it.
        self.maze = []
        self.start = (0,0) # location of '<' in self.maze in row,column coordinates
        self.end = (0,0) # location of '>' in self.maze in row,column coordinates

        currentrow = 0
        with open(filename, 'r') as f:
            first = True
            for l in f:
                # the first row of maze files gives the columns and rows in the maze
                if first:
                    first = False
                    dims = l.split(',')
                    cols, rows = int(dims[0]), int(dims[1])
                    self.maze = [[]] * rows
                    for i in range(rows):
                        self.maze[i] = ['#'] * cols
                else:
                    for i, c in enumerate(l):
                        if i >= cols:
                            break
                        self.maze[currentrow][i] = c
                        if c == '<':
                            self.start = (currentrow, i)
                        if c == '>':
                            self.end = (currentrow, i)

                    currentrow += 1
                    if currentrow >= rows:
                        break

    # Moves can only happen up down left or right, and cannot run through walls.
    # y, x is where you want to move from
    # dy, dx is how you want to move:
    #    dy = 0 dx = 1 means 1 column to the right
    #    dy = -1 dx = 0 means 1 row UP, since we read the maze in print order
    def canMove(self, y, x, dy, dx):
        if dx != 0 and dy != 0:
            return False
        if abs(dx) > 1 or abs(dy) > 1:
            return False
        if (x < 0 or x >= len(self.maze[0]) # all rows have the same number of columns
                or y < 0 or y >= len(self.maze) # rows are the outer array of arrays
                or x + dx < 0
                or y + dy < 0
                or x + dx >= len(self.maze[0])
                or y + dy >= len(self.maze)):
            return False
        if self.maze[y][x] == '#':
            return False
        # This currently only checks for open space and terminals.  If you're adding other
        # markings in the grid you may want to alter this.
        return self.maze[y + dy][x + dx] in [' ', '<', '>']

    def solve(self):
        # TODO Implement me
        self.printMaze()

    def printMaze(self):
        for line in self.maze:
            for cell in line:
                print(cell, end='')
            print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please pass a maze file.')
    else:
        m = Maze(sys.argv[1])
        m.solve()
