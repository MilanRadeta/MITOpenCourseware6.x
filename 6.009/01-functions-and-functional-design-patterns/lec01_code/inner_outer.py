x = 0

def outer():
    x = 1
    def inner():
        print('inner:', x)
    inner()
    print('outer:', x)


print('global:', x)
outer()
inner()
print('global:', x)

