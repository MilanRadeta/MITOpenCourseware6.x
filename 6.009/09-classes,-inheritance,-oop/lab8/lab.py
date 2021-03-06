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

    def simplify (self):
        return self
    
    def eval(self, mapping):
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
            return Num(0)
        return Num(1)
    
    def eval(self, mapping):
        return mapping.get(self.name, self)


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
        return Num(0)
    
    def eval(self, mapping):
        return self.n

class BinOp(Symbol):
    def __init__(self, operator, left, right, priority=1):
        """
        Initializer.  Store an instance variable called `operator`, containing the
        binary operator symbol, and `left` and `right` operands.
        """
        self.operator = operator
        self.priority = priority
        self.left = BinOp.process_operands(left)
        self.right = BinOp.process_operands(right)
        self.simple_left = self.left.simplify()
        self.simple_right = self.right.simplify()

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
        return operand

    def parenthesize_operands(self, operand, check_same_precedence=False):
        """
        Parenthesize operands if needed by checking their precedence
        """
        if isinstance(operand, BinOp):
            if operand.priority > self.priority:
                return '(%s)' % operand
            if check_same_precedence and type(self) in (Div, Sub) and operand.priority == self.priority:
                return '(%s)' % operand
        return operand
        

    def __str__(self):
        left = self.parenthesize_operands(self.left)
        right = self.parenthesize_operands(self.right, True)
        return '%s %s %s' % (left, self.operator, right)

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, repr(self.left), repr(self.right))

    def has_two_number_operands(self):
        return isinstance(self.simple_left, Num) and isinstance(self.simple_right, Num)

    def check_value(self, val, is_commutative=True, is_zero_check=False):
        left = self.simple_left
        right = self.simple_right
        if (is_zero_check or is_commutative) and isinstance(left, Num) and left.n == val:
            return Num(0) if is_zero_check else right
        if isinstance(right, Num) and right.n == val:
            return Num(0) if is_zero_check else left
        return None if is_zero_check else self.__class__(left, right)


class Add(BinOp):
    def __init__(self, left, right):
        super().__init__('+', left, right, 2)

    def deriv(self, var):
        return Add(self.left.deriv(var), self.right.deriv(var))

    def simplify (self):
        if self.has_two_number_operands():
            return Num(self.simple_left.n + self.simple_right.n)
        return self.check_value(0)
    
    def eval(self, mapping):
        return self.simple_left.eval(mapping) + self.simple_right.eval(mapping)

class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__('-', left, right, 2)

    def simplify (self):
        if self.has_two_number_operands():
            return Num(self.simple_left.n - self.simple_right.n)
        return self.check_value(0, False)
    
    def eval(self, mapping):
        return self.simple_left.eval(mapping) - self.simple_right.eval(mapping)
    

class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__('*', left, right)

    def deriv(self, var):
        return Add(Mul(self.left, self.right.deriv(var)), Mul(self.right, self.left.deriv(var)))

    def simplify (self):
        if self.has_two_number_operands():
            return Num(self.simple_left.n * self.simple_right.n)
        return self.check_value(0, is_zero_check=True) or self.check_value(1)
    
    def eval(self, mapping):
        return self.simple_left.eval(mapping) * self.simple_right.eval(mapping)

class Div(BinOp):
    def __init__(self, left, right):
        super().__init__('/', left, right)

    def deriv(self, var):
        return Div(Sub(Mul(self.right, self.left.deriv(var)), Mul(self.left, self.right.deriv(var))), Mul(self.right, self.right))

    def simplify (self):
        if self.has_two_number_operands():
            return Num(self.simple_left.n / self.simple_right.n)
        return self.check_value(0, is_zero_check=True) or self.check_value(1, False)
    
    def eval(self, mapping):
        return self.simple_left.eval(mapping) / self.simple_right.eval(mapping)
    
def tokenize(input):
    res = []
    last_val = ''
    input = input.strip()
    if input[0] != '(':
        input = '(' + input + ')'

    def parse_val():
        try:
            if '.' in last_val:
                res.append(float(last_val))
            else:
                res.append(int(last_val))
        except:
            res.append(last_val)

    for char in input:
        if char == ' ':
            continue
        if char in ('(',')','*','/'):
            if last_val:
                parse_val()
                last_val = ''
            res.append(char)
        elif char in ('+', '-'):
            if last_val:
                parse_val()
                res.append(char)
                last_val = ''
            elif len(res) == 0 or res[-1] in ('(', '*', '/', '+', '-'):
                last_val += char
            else:
                res.append(char)
        else:
            last_val += char
    if last_val:
        parse_val()
            

    return res

def parse(tokens):
    token_ops = {
        '+': Add,
        '-': Sub,
        '*': Mul,
        '/': Div,
    }
    
    def parse_expression(index):
        token = tokens[index]
        if token == '(':
            left, next_index = parse_expression(index + 1)
            if next_index + 1 < len(tokens):
                op = tokens[next_index]
                right, next_index = parse_expression(next_index + 1)
                return token_ops[op](left, right), next_index + 1
            return left, next_index + 1
        else:
            try:
                if token > 0 or token <= 0:
                    return Num(token), index +1
            except:
                pass
            return Var(token), index + 1
    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

def sym(exp):
    return parse(tokenize(exp))


if __name__ == '__main__':
    doctest.testmod()
