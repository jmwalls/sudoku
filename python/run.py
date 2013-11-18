#!/usr/bin/env python
import time

from sudoku import *

solvemeth = 'rand'

def solve (puzz):
    p = parse_from_string (puzz)
    print 'solving puzzle...',
    start = time.clock ()
    p.solve (solvemeth)
    t = time.clock ()-start
    print '%0.3f seconds' % t
    return t

dpath = '../data/sudoku.txt'
puzz, soltimes = [], []
with open (dpath, 'r') as f:
    for l in f:
        if 'Grid' in l:
            if not len (puzz): continue
            soltimes.append (solve (''.join (puzz)))
            puzz[:] = []
        else:
            puzz.append (l)
if len (puzz):
    soltimes.append (solve (''.join (puzz)))

npuzz = len (soltimes)
tavg = sum (soltimes)/npuzz
print 'solved %d puzzles with an average time %0.3f seconds' % (npuzz,tavg)
