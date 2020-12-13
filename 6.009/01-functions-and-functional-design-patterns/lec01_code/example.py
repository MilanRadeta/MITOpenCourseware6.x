x = 500
def foo(y):
    return x + y
z = foo(307)

print('x:', x)
print('foo:', foo)
print('z:', z)

def bar(x):
    x = 1000
    return foo(308)

w = bar('hello')
print()
print('x:', x)
print('w:', w)
