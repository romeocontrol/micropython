(x := 4)
print(x)

if x := 2:
    print(True)
print(x)

print(min(4, x := 5))
print(x)

x = 1
print(min(x, x := 5))
print(x)

def foo():
    print('any', any((hit := i) % 5 == 3 and (hit % 2) == 0 for i in range(10)))
    return hit

hit = 123
print(foo())
print(hit) # shouldn't be changed by foo

print('any', any((hit := i) % 5 == 3 and (hit % 2) == 0 for i in range(10)))
print(hit) # should be changed by above

print([i := i + 1 for i in range(4)])
print(i)
del i

print([i := -1 for i, j in [(1, 2)]])
print(i)

print([((m := k + 1), k * m) for k in range(4)])

# j doesn't exist
try:
    print([[(j := j) for i in range(2)] for j in range(2)])
except NameError:
    print('NameError')

# j is a global
j = 9
print([[(j := j) for i in range(2)] for j in range(2)])
print(j)
