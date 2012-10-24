#!/usr/bin/env python

# just some example code that parses our maze pgm format

import sys

items = []
for line in open('../data/maze1.pgm', 'r'):
    comment_index = line.find('#')
    if comment_index != -1:
        line = line[:comment_index]

    items.extend(line.split())

if items[0] != 'P2':
    print "Error: PGM file must start with 'P2'"
    sys.exit(-1)

width = int(items[1])
height = int(items[2])

# items[3]: max value of "colors"; ignore

items = items[4:]

maze = [[int(items[j * width + i]) for i in range(width)] for j in range(height)]

for row in maze:
    print ' '.join([str(i) for i in row])

