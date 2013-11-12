"""
base Sudoku puzzle representation and utility functions for reading/printing
puzzles
"""

from copy import deepcopy
from random import randint

ROWS = 'ABCDEFGHI'
COLS = '012345678'
VALS = '123456789'

def cross (A, B):
    return [a+b for a in A for b in B]

SQUARES = cross (ROWS, COLS)
UNITS = [cross (r, COLS) for r in ROWS] +\
        [cross (ROWS, c) for c in COLS] +\
        [cross (r,c) for r in ('ABC','DEF','GHI') for c in ('012','345','678')]
PEERS = dict ((s,[i for u in UNITS if s in u for i in u if i != s]) for s in SQUARES)

class Sudoku (object):
    """
    Sudoku object implements the state of a puzzle

    Parameters
    -----------
    squares : dict of square id to list of values
    """
    def __init__ (self, givens=None):
        """
        construct Sudoku object

        Parameters
        -----------
        givens : 81-element list of given squares
        """
        self.squares = {s:VALS for s in SQUARES}

        if givens is None: return
        for sq, g in zip (SQUARES,givens):
            self.set_square (sq,g)

    def set_square (self, sq, val):
        """
        set value of square and eliminate value from square's peers

        Parameters
        -----------
        sq : square id
        val : value of square
        """
        if not val in VALS: return
        if not val in self.squares[sq]:
            raise Exception ('value has already been eliminated!')
        remain = self.squares[sq].replace (val,'')
        for r in remain: self.eliminate (sq,r)

    def eliminate (self, sq, val):
        """
        eliminate val from square

        Parameters
        -----------
        sq : square id
        val : value of square
        """
        if not val in self.squares[sq]: return
        self.squares[sq] = self.squares[sq].replace (val,'')
        if len (self.squares[sq]) == 0:
            raise Exception ('contradiction! no values remain in square')
        elif len (self.squares[sq]) == 1:
            v = self.squares[sq]
            for p in PEERS[sq]: self.eliminate (p,v)

    def _complete (self):
        """
        checks if all squares have only a single value
        """
        for v in self.squares.itervalues ():
            if len (v) > 1: return False
        return True

    def solve (self, method='rand'):
        """
        solve puzzle---for now, lets just guess

        Parameters
        -----------
        method : solve routine to use, excepted values are {'rand', 'dfs'}

        Returns
        --------
        True if unique solution found
        """
        if method=='rand': 
            self._solve_random ()
        else:
            raise Exception ('unknown solve routine requested!')
        return self._complete ()

    def _solve_random (self):
        """
        randomly guess correct configuration until we find the solution
        """
        squares = deepcopy (self.squares)
        iters = 0
        while True:
            if self._complete (): break
            errs, sq = min ((len (v), s) for s,v in self.squares.iteritems () if len (v)>1)
            try:
                vals = self.squares[sq]
                ii = randint (0,len (vals)-1)
                self.eliminate (sq, vals[ii])
            except:
                self.squares = deepcopy (squares)
            iters += 1
        print '%d iters' % iters

    def _solve_dfs (self):
        """
        DFS
        """
        raise NotImplemented ('DFS not implemented!')

    def display (self):
        """
        nicely prind puzzle
        """
        width = 1+ max (len (v) for v in self.squares.itervalues ())
        sep = '+'.join (3*[3*width*'-'])
        for r in ROWS:
            print ''.join (self.squares[r+c].center (width)+
                    ('|' if c in '25' else '') for c in COLS)
            if r in 'CF': print sep


def parse_from_string (s):
    """
    parse puzzle from string

    Parameters
    -----------
    s : puzzle string

    Returns
    --------
    p : Sudoku instance
    """
    givens = [c for c in s if c in VALS or c in '0.']
    p = Sudoku (givens)
    return p

def parse_from_file (fname):
    """
    parse puzze from file

    Parameters
    -----------
    fname : filename of puzzle

    Returns
    --------
    p : Sudoku instance
    """
    with open (fname, 'r') as f:
        s = f.read ().strip ()
    p = parse_from_string (s)
    return p

if __name__ == '__main__':
    import sys

    if len (sys.argv) < 2:
        print 'usage: %s <puzzle.txt>' % sys.argv[0]
        sys.exit (0)

    try:
        p = parse_from_file (sys.argv[1])
    except Exception as e:
        print 'error opening puzzle!'

    print 'loaded puzzle:'
    p.display ()

    print '\n\nsolving...',
    if p.solve (): print 'found unique solution'
    else: print 'could not find solution'
    p.display ()

    sys.exit (0)
