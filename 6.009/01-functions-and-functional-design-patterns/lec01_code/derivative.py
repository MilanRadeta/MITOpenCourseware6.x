def deriv(f, dx=1e-3):
    def _fprime(x):
        return (f(x+dx) - f(x-dx)) / (2*dx)
    return _fprime


def foo(x):
    return 3 * x**3

print(foo(4))

df = deriv(foo) # 9 * x**2
print(df(4))
