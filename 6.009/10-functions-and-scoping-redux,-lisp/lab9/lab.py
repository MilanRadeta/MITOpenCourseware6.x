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
            current.append(val)
        i += 1
    return res


######################
# Built-in Functions #
######################


snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
}


##############
# Evaluation #
##############


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if isinstance(tree, str) and tree in snek_builtins:
        return snek_builtins[tree]
    if type(tree) in (int, float):
        return tree
    if isinstance(tree, list):
        fun = tree[0]
        if fun not in snek_builtins:
            raise SnekEvaluationError
        args = [evaluate(arg) for arg in tree[1:]]
        return snek_builtins[fun](args)
    raise SnekNameError


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    while True:
        inp = input('in> ')
        if inp == 'QUIT':
            break
        try:
            print('  out>', evaluate(parse(tokenize(inp))))
        except Exception as e:
            print('  out>', e)
