#!/usr/bin/env python
from sudoku import *

dpath = '../data/sudoku.txt'
with open (dpath, 'r') as f:
    puzz = []
    for l in f:
        if 'Grid' in l:
            if not len (puzz): continue
            p = parse_from_string (''.join (puzz))
            print 'solving puzzle...',
            p.solve ()
            puzz[:] = []
        else:
            puzz.append (l)
