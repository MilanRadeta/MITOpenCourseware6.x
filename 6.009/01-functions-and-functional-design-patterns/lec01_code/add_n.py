def add_n(n):
    def inner(x):
        return x + n
    return inner

add1 = add_n(1)
add2 = add_n(2)

print(add2(3))
print(add1(7))
print(add_n(8)(9))
