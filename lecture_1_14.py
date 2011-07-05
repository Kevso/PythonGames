#!/usr/bin/env python
def many(name, *values):
    print name, values

args = input('Gimme some juice!: ')
many(args[0], [arg for arg in args[1:]])
