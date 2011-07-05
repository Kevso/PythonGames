#!/usr/bin/env python
rows = int(raw_input('Rows: '))
columns = int(raw_input('Columns: '))
first_row = [2 * i + 1 for i in range(columns)]

def build_row(row_num):
    if row_num == 0: return first_row
    else:
        transform = lambda column_val: (row_num+1) * column_val + 1 
        return map(transform, first_row)

matrix = []
for row_num in range(rows):
    matrix.append(build_row(row_num))

print matrix
