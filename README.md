##Sudoku solver
===============

Just playing around with a few different ideas to complete Sudoku puzzles.
Methods include

* Random guessing: prune search space based on givens, randomly guess
  remaining solutions until we have a solution.
* Constraint satisfaction: prune the search space based on given squares and
  then search the remaining candidate solutions.
* Bayesian inference via belief propagation: solve for the maximum a
  posteriori solution conditioned on the given squares. (loopy) Belief
  propagation allows us efficiently compute the solution without tracking the
  full discrete distribution over puzzle states.

###Organization
--------

python : contains all code  
data : contains puzzles  

###Puzzles
--------
Puzzles are provided by [Project Euler](http://projecteuler.net/index.php?section=problems&id=96)


###Authors
--------
Jeff Walls <jmwalls@umich.edu>
