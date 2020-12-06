import numpy


def inputNumber(varName):
    try:
        return int(input(f"Enter number {varName}: "))
    except:
        print('ERROR: That was not a number')
        exit(-1)


x = inputNumber('x')
y = inputNumber('y')
print(f'x^y = {x**y}')
print(f'log2(x) = {numpy.log2(x)}')
