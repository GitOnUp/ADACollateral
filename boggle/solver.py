#!/usr/bin/env python3
from trie import Trie
import math
import sys


class Tile(object):
    def __init__(self, char):
        self.char = char
        self.visited = False
        self.neighbors = [None] * 8


NEIGHBOR_IDX = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0)
]


class Board(object):
    def __init__(self, chars, dictionary, size=4):
        self.trie = Trie()
        for word in dictionary:
            self.trie.insert(word)

        self.tiles = [None] * size
        for i in range(size):
            self.tiles[i] = [None] * size
        ixchar = 0
        for y in range(size):
            for x in range(size):
                self.tiles[y][x] = Tile(chars[ixchar].lower())
                ixchar += 1
        for y in range(size):
            for x in range(size):
                for i, nix in enumerate(NEIGHBOR_IDX):
                    nx, ny = nix
                    if 0 <= nx + x < size and 0 <= ny + y < size:
                        self.tiles[y][x].neighbors[i] = self.tiles[ny + y][nx + x]

    def solve(self):
        words = set()  # I was wrong last week: Python has sets but it didn't always (v2.3).
        i = self.trie.iterate()
        sideSize = len(self.tiles)
        for iTile in range(sideSize * sideSize):
            self.solveFromTile(i, self.tiles[iTile // sideSize][iTile % sideSize], words)
        return words

    def solveFromTile(self, i, tile, words):
        tile.visited = True
        if i.advance(tile.char):
            if i.isWord():
                words.add(i.value())
            for n in tile.neighbors:
                if n is not None and not n.visited:
                    self.solveFromTile(i, n, words)
            i.pop()
        tile.visited = False


def usage():
    print("Enter letters on a board separated by spaces, reading left to right, then down lines.")
    print("For example, the board:")
    print()
    print("  a b c")
    print("  d e f")
    print("  g h i")
    print()
    print("Is specified by typing:")
    print("  a b c d e f g h i")
    print()
    print("Boards must be square.")
    print("Control+D exits.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please run with a dictionary file as an argument.')
        exit()

    with open(sys.argv[1], 'r') as f:
        print('Loading words...', end='')
        d = set()
        for w in f:
            d.add(w.strip())
        print('done')

    print()
    usage()
    while True:
        try:
            line = input('> ')
            chars = line.strip().split(' ')
            size = math.sqrt(len(chars))
            if size * size != math.floor(size) * math.floor(size):
                print('A square number of tiles is needed.')
                continue
            for c in chars:
                if len(c) > 1:
                    usage()
                    continue

            b = Board(chars, d, int(size))
            found = b.solve()
            print()
            print('Found the following words:')
            print()
            found = sorted(found)
            print(sorted(found, key=len, reverse=True))
            print()
            print('%s words found.' % len(found))
        except EOFError as e:
            break
        except Exception as e:
            print("Unexpected " + str(e))
    print()
