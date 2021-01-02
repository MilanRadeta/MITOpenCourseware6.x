import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    pass


class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'


class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'

class BinOp(Symbol):
    def __init__(self, operator, left, right):
        """
        Initializer.  Store an instance variable called `operator`, containing the
        binary operator symbol, and `left` and `right` operands.
        """
        self.operator = operator
        self.left = BinOp.process_operator(left)
        self.right = BinOp.process_operator(right)

    @staticmethod
    def process_operator(operator):
        """
        Processes operator to adequate Symbol
        """
        if type(operator) is str:
            return Var(operator)
        if type(operator) in (float, int):
            return Num(operator)
        if not isinstance(operator, Symbol):
            raise TypeError

    def __str__(self):
        return '%s %s %s' % (self.left, self.operator, self.right)

    def __repr__(self):
        return 'BinOp(%s, %s, %s)' % (self.operator, repr(self.left), repr(self.right))

class Add(BinOp):
    def __init__(self, left, right):
        super().__init__('+', left, right)

class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__('-', left, right)

class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__('*', left, right)

class Div(BinOp):
    def __init__(self, left, right):
        super().__init__('/', left, right)
    


if __name__ == '__main__':
    doctest.testmod()
