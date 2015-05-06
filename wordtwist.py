#!/usr/bin/env python3
from copy import copy
import readline
import string
import sys


class Iteration(object):
    def __init__(self, prevs, word):
        self.prevs = prevs
        self.word = word

    def next(self, word):
        newprevs = self.prevs[:]
        newprevs.append(self.word)
        return Iteration(newprevs, word)


class Data(object):
    def __init__(self, filename):
        self._wordlens = []
        with open(filename) as f:
            for line in f:
                self._addword(line.strip())

    def _addword(self, word):
        if len(self._wordlens) < len(word):
            self._wordlens.extend([{}] * (len(word) - len(self._wordlens)))
            self._wordlens[len(word)-1] = {}
        self._wordlens[len(word)-1][word] = True

    def twist(self, startword, endword):
        length = len(startword)
        if len(startword) != len(endword):
            raise ValueError()
        working = copy(self._wordlens[length-1])
        iterations = [Iteration(list(), startword)]
        while len(iterations) > 0:
            iteration = iterations.pop(0)
            for ichar in range(0, length):
                for char in string.ascii_lowercase:
                    newword = iteration.word[:ichar] + char + iteration.word[ichar+1:]
                    if newword != iteration.word and working.get(newword, False):
                        del working[newword]
                        newiteration = iteration.next(newword)
                        if newword == endword:
                            return newiteration.prevs + [newword]
                        iterations.append(newiteration)
        return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s <dictionaryfile>' % sys.argv[0])
        print('  gives path from one word to another by changing one char at a time.')
        sys.exit()

    print("Loading...")
    data = Data(sys.argv[1])
    print("Done, enter words.  Control+D ends.")
    while True:
        try:
            line = input('> ')
            words = line.strip().split(' ')
            if len(words) != 2:
                print("Enter two words.  Control+D ends.")
                continue
            print(data.twist(words[0].strip(), words[1].strip()))
        except ValueError as e:
            print("Words must be the same length.")
        except EOFError as e:
            break
        except Exception as e:
            print("Unexpected " + str(e))
    print()
