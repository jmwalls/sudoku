##Sudoku solver
===============

Just playing around with a few different ideas to complete Sudoku puzzles.
Methods include

* Search: prune the search space based on givens and then search the remaining
  space until we find a valid solution. We'll try a few different search
  techniques: depth first search, guess and check.
* Constraint satisfaction: apply a few different constraint programming
  algorithms including simulated annealing.
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
