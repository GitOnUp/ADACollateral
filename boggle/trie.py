class TrieNode(dict):
    def __init__(self):
        super(TrieNode, self).__init__()
        self.isWord = False


class Iterator(object):
    def __init__(self, parent):
        self._parent = parent
        self._node = parent._root
        self._nodes = []
        self._value = ''

    def advance(self, char):
        next = self._node.get(char, None)
        if next is not None:
            self._nodes.append(self._node)
            self._node = next
            self._value += char
            return True
        return False

    def isWord(self):
        return self._node.isWord

    def reset(self):
        self._node = self.parent._root
        self._nodes = []
        self._value = ''

    def value(self):
        return self._value

    def pop(self):
        if len(self._nodes):
            self._node = self._nodes[-1]
            self._nodes.pop()
            self._value = self._value[:-1]


class Trie(object):
    def __init__(self):
        self._root = TrieNode()

    def iterate(self):
        return Iterator(self)

    def insert(self, word):
        i = self.iterate()
        adding = False
        for c in word:
            if not adding:
                if i.advance(c):
                    continue
                else:
                    adding = True
            i._node[c] = TrieNode()
            i.advance(c)
        i._node.isWord = True


if __name__ == "__main__":
    trie = Trie()
    trie.insert('ada')
    trie.insert('apple')
    trie.insert('banana')

    i = trie.iterate()
    assert not i.isWord()
    assert i.advance('a')
    assert i.advance('d')
    assert not i.advance('b')
    assert not i.isWord()
    assert i.advance('a')
    assert i.isWord()