#!/usr/bin/env python
height = input('Height: ')
width = input('Width: ')
for row in range(height):
    if row == 0 or row == height-1:
        print '@' * width
    else:
        print '@' + (' ' * (width-2)) + '@'
