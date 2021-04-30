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


def validate_token(tokens, i):
    val = tokens[i]
    if val == 'define':
        name = tokens[i+1]
        expr = tokens[i+2]
        try: 
            int(name)
            raise SnekSyntaxError
        except:
            if expr in snek_builtins or expr == ')':
                raise SnekSyntaxError

    if val == 'lambda':
        i += 1
        if tokens[i] != '(':
            raise SnekSyntaxError
        i += 1
        while True:
            val = tokens[i]
            if type(val) in (int, float):
                raise SnekSyntaxError
            if val == ')':
                break
            i += 1
        val = tokens[i]
        if type(val) in (int, float):
            raise SnekSyntaxError
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
            raise SnekSyntaxError
        try:
            return float(token) if '.' in token else int(token)
        except:
            return token
        
    if tokens[0] != '(' or tokens[-1] != ')':
        raise SnekSyntaxError
    
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
            if len(nested) > 0:
                val = nested.pop()
                current = nested[-1] if len(nested) > 0 else res
                current.append(val)
            else:
                raise SnekSyntaxError
        else:
            try:
                val = float(token) if '.' in token else int(token)
            except:
                val = token
                try:
                    validate_token(tokens, i)
                except:
                    raise SnekSyntaxError
            current.append(val)
        i += 1
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
        raise SnekEvaluationError
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
            if isinstance(tree[1], list):
                tree[2] = ['lambda', tree[1][1:], tree[2]]
                tree[1] = tree[1][0]
            env[tree[1]] = evaluate(tree[2], env)
            return env[tree[1]]
        if fun == 'lambda':
            return UserDefinedFun(env, tree[1], tree[2])
        if isinstance(fun, str):
            if fun not in env:
                raise SnekEvaluationError
            fun = env[fun]

        args = [evaluate(arg, env) for arg in tree[1:]]
        try:
            return fun(args)
        except:
            raise SnekEvaluationError
    raise SnekNameError


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
        raise SnekNameError
    
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
            print('  out>', type(e).__name__)
