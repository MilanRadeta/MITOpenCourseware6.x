class LinkedList:
    def __init__(self, val, sublist=None):
        self.val = val
        self.sublist = sublist

    def get(self, index):
        if index == 0:
            return self.val
        if self.sublist is None:
            raise IndexError()
        return self.sublist.get(index - 1)

    def set(self, index, value):
        if index == 0:
            self.val = value
        elif self.sublist is None:
            raise IndexError()
        else:
            self.sublist.set(index - 1, value)

    def elements(self):
        yield self.val

        if self.sublist is not None:
            for e in self.sublist.elements():
                yield e

    def __str__(self):
        s = '[ '
        for e in self.elements():
            s += str(e) + ', '
        s = s[:-2] + ' ]'
        return s

    def __repr__(self):
        return 'LinkedList(%s, %s)' % (self.val, repr(self.sublist))

    def append(self, elt):
        if self.sublist is None:
            self.sublist = LinkedList(elt)
        else:
            self.sublist.append(elt)

    def length(self):
        if self.sublist is None:
            return 1
        return 1 + self.sublist.length()

    def insert(self, index, elt):
        if index == 0:
            self.sublist = LinkedList(self.val, self.sublist)
            self.val = elt
        elif self.sublist is None:
            raise IndexError()
        else:
            self.sublist.insert(index - 1, elt)

    def delete(self, index):
        if self.sublist is None:
            raise IndexError()
        elif index > 1:
            self.sublist.delete(index - 1)
        elif index == 1:
            self.sublist = self.sublist.sublist
        elif index == 0:
            self.val = self.sublist.val
            self.sublist = self.sublist.sublist


x = LinkedList(4,
        LinkedList(8,
            LinkedList(15,
                LinkedList(16,
                    LinkedList(23,
                        LinkedList(42))))))

print(x)
print(repr(x))
print('Length: ', x.length())
print(x.get(0), x.get(3), x.get(5))
try:
    print(x.get(6))
except IndexError:
    pass
for elem in x.elements():
    print(elem)
x.set(0, 0)
x.set(3, 3)
x.set(5, 5)
print(x)
x.append(6)
print(x)
x.insert(6, 7)
print(x)
x.delete(6)
print(x)
x.delete(6)
print(x)
x.delete(0)
print(x)
x.insert(0, -1)
print(x)
x.delete(0)
print(x)