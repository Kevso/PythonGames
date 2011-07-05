#!/usr/bin/env python
def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

n = int(raw_input('How many fibonacci numbers?: '))
for i in range(n):
    print fib(i),
