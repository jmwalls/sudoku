"""
base Sudoku puzzle representation and utility functions for reading/printing
puzzles
"""

from copy import deepcopy
import numpy as np

from simanneal import Simanneal

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

MAXITERS = 1e6

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

        self.givens = {}
        if givens is None: return
        for sq, g in zip (SQUARES,givens):
            self.set_given (sq,g)
        if self._complete (): print '{Sudoku}: puzzle solved already!'

    def set_given (self, sq, val):
        """
        set value of square and eliminate value from square's peers

        Parameters
        -----------
        sq : square id
        val : value of square
        """
        if not val in VALS: return
        self.givens[sq] = val

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
        elif method=='dfs':
            self._solve_dfs ()
        elif method=='simanneal':
            self._solve_anneal ()
        elif method=='loopy':
            self._solve_loopy ()
        else:
            raise Exception ('unknown solve routine requested!')
        return self._complete ()

    def _solve_random (self):
        """
        Randomly guess correct value for the square with the fewest candidate
        values until we're right. 
        
        If we encounter an invalid configuration, start over.

        Essentially, a slightly more principled bogo search---we are allowed
        to try the same wrong configuration multiple times.
        """
        squares = deepcopy (self.squares)
        iters = 0
        while not self._complete ():
            errs, sq = min ((len (v), s) for s,v in self.squares.iteritems ()
                    if len (v)>1)
            try:
                vals = self.squares[sq]
                ii = np.random.randint (0,len (vals))
                self.eliminate (sq, vals[ii])
            except:
                self.squares = deepcopy (squares)
            if iters>MAXITERS:
                raise Exception ("Random solution routine exceeded maximum allowable iterations")
            iters += 1

    def _solve_dfs (self):
        """
        Search configuration space beginning with square with fewest candidate
        values.

        If we encounter an invalid configuration, recurse back up the search
        tree.

        Probably faster (in general) than _solve_random because we can only
        try a single incorrect configuration once.
        """
        raise NotImplemented ('DFS not implemented!')

    def _solve_anneal (self):
        """
        Apply simulated annealing to solve the puzzle:
        1. populate the remaining board with the usable set of digits, C_0
        2. while not solved:
        3.   choose a neighboring configuration, C
        4.   if c (C)<c (C_{n}) or U < exp ((c (C_{n}) - c (C))/T)
        5.      C_{n+1} = C 
        6.   update (T)

        The cost (c) and neighbor functions generators are also defined below.

        Parameters
        -----------
        vals : board configuration stored as an n**2 array
        """
        # populate board with remaining values
        rvals = 9*range (1,10)
        vals = np.zeros (9*9)
        for sq,g in self.givens.iteritems ():
            r,c = ROWS.find (sq[0]), COLS.find (sq[1])
            vals[9*r + c] = g
            rvals.remove (int (g))
        index = np.where (vals==0)[0]
        for ii in index: vals[ii] = rvals.pop (0)

        # the cost associated with a layout is the number of constraint
        # violations
        def cost (v):
            rcons = [9 - len (np.unique (vals[9*r:9*(r+1)])) for r in range (9)]
            ccons = [9 - len (np.unique (vals[c::9])) for c in range (9)]
            #bcons = [len (np.unique (b)) for b in vals]
            bcons = []
            return sum (rcons) + sum (ccons) + sum (bcons)

        # a neighbor swaps two cells
        def nbrs (v):
            return v

        # 2. optimize
        opt = Simanneal (cost,nbrs,vals)
        #iters = 0
        #while iters < 10:
        #    opt.next ()
        #    iters += 1

    def _solve_loopy (self):
        """
        """
        raise NotImplemented ('Loopy belief propagation not implemented!')

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
    import time

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
    start = time.clock ()
    if p.solve ('simanneal'): 
        print 'found a solution'
    else: 
        print 'could not find solution'
    print 'spun for %0.3f seconds' % (time.clock ()-start)
    #p.display ()

    sys.exit (0)
