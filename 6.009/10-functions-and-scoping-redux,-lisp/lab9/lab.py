#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!


###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass


class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass


class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    pass


############################
# Tokenization and Parsing #
############################


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    """
    res = []
    last_val = ''
    skip = False

    for char in source:
        if char in '(); \n' and last_val:
            res.append(last_val)
            last_val = ''
        if char == ';':
            skip = True
        elif char == '\n':
            skip = False
        elif skip or char == ' ':
            continue
        elif char in '()':
            res.append(char)
        else:
            last_val += char
    if last_val:
        res.append(last_val)

    return res


def validate_token(tree):
    if (len(tree) == 0):
        return
    if tree[0] == 'define':
        if (len(tree) != 3):
            raise SnekSyntaxError('Invalid definition')

        if isinstance(tree[1], list):
            if (len(tree[1]) == 0):
                raise SnekSyntaxError('Empty body')

            tree[2] = ['lambda', tree[1][1:], tree[2]]
            validate_token(tree[2])
            tree[1] = tree[1][0]
        name = tree[1]
        if type(name) in (int, float):
            raise SnekSyntaxError(name)

    if tree[0] == 'lambda':
        if (len(tree) != 3):
            raise SnekSyntaxError('Invalid lambda definition')
        params = tree[1]
        
        if not isinstance(params, list):
            raise SnekSyntaxError('Missing lambda parameters parenthesis')
        for arg in params:
            if type(arg) in (int, float):
                raise SnekSyntaxError(arg)
    return True

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    if len(tokens) == 1:
        token = tokens[0]
        if token in '()':
            raise SnekSyntaxError('Unneccessary parenthesis ' + token)
        try:
            return float(token) if '.' in token else int(token)
        except:
            return token
        
    if tokens[0] != '(':
        raise SnekSyntaxError('Missing opening parenthesis')
    if tokens[-1] != ')':
        raise SnekSyntaxError('Missing closing parenthesis')
    
    res = []
    nested = []
    current = res
    i = 1
    while i < len(tokens) - 1:
        token = tokens[i]
        if token == '(':
            nested.append([])
            current = nested[-1]
        elif token == ')':
            if (len(nested) == 0):
                raise SnekSyntaxError('Missing opening parenthesis')
            val = nested.pop()
            validate_token(val)
            current = nested[-1] if len(nested) > 0 else res
            current.append(val)
        else:
            try:
                val = float(token) if '.' in token else int(token)
            except:
                val = token
            current.append(val)
        i += 1
    validate_token(current)
    return res


######################
# Built-in Functions #
######################

def mul(args):
    res = 1
    for arg in args:
        res *= arg
    return res

def div(args):
    if len(args) == 0:
        raise SnekEvaluationError('Empty args')
    if len(args) == 1:
        return 1 / args[0]
    
    res = args[0] / args[1]

    for arg in args[2:]:
        res /= arg
    return res

snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': mul,
    '/': div,

}


##############
# Evaluation #
##############


def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if env is None:
        env = Environment(BuiltInsEnv)
    if isinstance(tree, str) and tree in env:
        return env[tree]
    if type(tree) in (int, float):
        return tree
    if isinstance(tree, list):
        fun = tree[0]
        if isinstance(fun, list):
            fun = evaluate(fun, env)

        if fun == 'define':
            env[tree[1]] = evaluate(tree[2], env)
            return env[tree[1]]
        if fun == 'lambda':
            return UserDefinedFun(env, tree[1], tree[2])
        if isinstance(fun, str):
            if fun not in env:
                raise SnekEvaluationError('Unknown function ' + fun)
            fun = env[fun]

        args = [evaluate(arg, env) for arg in tree[1:]]
        try:
            return fun(args)
        except Exception as e:
            if type(e) in [SnekSyntaxError, SnekNameError, SnekEvaluationError]:
                raise e
            raise SnekEvaluationError(tree)
    raise SnekNameError(tree[0])


class Environment():
    def __init__(self, parent=None, vars=None):
        self.parent = parent
        self.vars = {} if vars is None else vars
    
    def __contains__(self, name: str):
        try:
            return self[name] and True
        except SnekNameError:
            return False

    def __getitem__(self, name: str):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent[name]
        raise SnekNameError(name)
    
    def __setitem__(self, name: str, value):
        self.vars[name] = value

BuiltInsEnv = Environment(None, snek_builtins)

def result_and_env(tree, env=None):
    if env is None:
        env = Environment(BuiltInsEnv)
    return evaluate(tree, env), env

class UserDefinedFun():
    def __init__(self, env, args, expr):
        self.env = env
        self.args = args
        self.expr = expr

    def __call__(self, *args, **kwargs):
        args = args[0]
        if len(self.args) != len(args):
            raise SnekEvaluationError
        env = Environment(self.env)
        for i in range(len(self.args)):
            env[self.args[i]] = args[i]
        return evaluate(self.expr, env)

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    env = None
    while True:
        inp = input('in> ')
        if inp == 'QUIT':
            break
        try:
            val, env = result_and_env(parse(tokenize(inp)), env)
            print('  out>', val)
        except Exception as e:
            print('  out>', type(e).__name__, e.args)
