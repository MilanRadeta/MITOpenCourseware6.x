import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __add__(self, other):
        return Add(self, other)
    def __radd__(self, other):
        return Add(other, self)
    def __sub__(self, other):
        return Sub(self, other)
    def __rsub__(self, other):
        return Sub(other, self)
    def __mul__(self, other):
        return Mul(self, other)
    def __rmul__(self, other):
        return Mul(other, self)
    def __truediv__(self, other):
        return Div(self, other)
    def __rtruediv__(self, other):
        return Div(other, self)

    def deriv(self, var):
        raise NotImplementedError



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

    def deriv(self, var):
        if var != self.name:
            return 0
        return 1


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

    def deriv(self, var):
        return 0

class BinOp(Symbol):
    def __init__(self, operator, left, right, precedence=1):
        """
        Initializer.  Store an instance variable called `operator`, containing the
        binary operator symbol, and `left` and `right` operands.
        """
        self.operator = operator
        self.precedence = precedence
        self.left = BinOp.process_operands(left)
        self.right = BinOp.process_operands(right)

    @staticmethod
    def process_operands(operand):
        """
        Processes operator to adequate Symbol
        """
        if type(operand) is str:
            return Var(operand)
        if type(operand) in (float, int):
            return Num(operand)
        if not isinstance(operand, Symbol):
            raise TypeError

    def parenthesize_operands(self, operand, check_same_precedence=False):
        """
        Parenthesize operands if needed by checking their precedence
        """
        if isinstance(operand, BinOp):
            if operand.precedence < self.precedence:
                return '(%s)' % operand
            if check_same_precedence and type(self) in (Div, Sub) and operand.precedence == self.precedence:
                return '(%s)' % operand
        return operand
        

    def __str__(self):
        left = self.parenthesize_operands(self.left)
        right = self.parenthesize_operands(self.right, True)
        return '%s %s %s' % (left, self.operator, right)

    def __repr__(self):
        return 'BinOp(%s, %s, %s)' % (self.operator, repr(self.left), repr(self.right))

class Add(BinOp):
    def __init__(self, left, right):
        super().__init__('+', left, right, 2)

    def deriv(self, var):
        return self.left.deriv(var) + self.right.deriv(var)

class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__('-', left, right, 2)

    def deriv(self, var):
        raise NotImplementedError
    

class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__('*', left, right)

    def deriv(self, var):
        return self.left * self.right.deriv(var) + self.right * self.left.deriv(var)

class Div(BinOp):
    def __init__(self, left, right):
        super().__init__('/', left, right)

    def deriv(self, var):
        return (self.right * self.left.deriv(var) - self.left * self.right.deriv(var)) / (self.right * self.right)
    


if __name__ == '__main__':
    doctest.testmod()
