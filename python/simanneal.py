import numpy as np

class Simanneal (object):
    """
    Basic simulated annealing optimizer---given a discrete configuration
    space, we seek the optimal value via randomized local search.

    Parameters
    -----------
    cost : user provided function that takes a configuration as an argument
        and returns the cost (must be a value that can be compared with less
        than)
    nbrs : user provided function that takes a configuration as an
        argument and returns a list of neighboring solutions
    temp : current temperature
    x : current configuration
    score : score of current configuration
    """
    def __init__ (self, cost, nbrs, x0, t0=1e2, alpha=0.99):
        """
        initialize simulated annealing problem

        Parameters
        -----------
        x0 : initial configuration
        """
        self.cost = cost
        self.nbrs = nbrs

        self.x = x0
        self.score = self.cost (self.x)

        self.iters = 0
        self.temp = t0
        self.alpha = alpha

    def next (self):
        """
        perform next optimization iteration
        """
        nbrs = self.nbrs (self.x)
        ii = np.random.randint (0,len (nbrs))
        xn = nbrs[ii]
        nscore = self.cost (xn)
        
        if self._accept (xn, nscore):
            self.x = xn
            self.score = nscore

        self._update ()
        return self.score

    def _accept (self, x, score):
        de = self.score - score
        p = 1. if de > 0 else np.exp (de/self.temp);

        pthreshold = np.random.rand ()
        if p > pthreshold: return True
        else: return False
    
    def _update (self):
        self.temp *= self.alpha
        self.iters += 1


if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt

    print 'testing simulated annealing...'
    data = np.cumsum (np.random.rand (1e4) - 0.5)

    def cost (x):
        return data[x]

    def nbrs (x):
        nd = []
        if x>0: nd.append (x-1)
        if x<len (data)-2: nd.append (x+1)
        nd.append (np.random.randint (0, len (data)))
        return nd

    opt = Simanneal (cost, nbrs, np.random.randint (0,len (data)))
    scores = []
    for ii in range (5000):
        scores.append (opt.next ())
    scores = np.asarray (scores)

    fig = plt.figure ()
    ax_data = fig.add_subplot (211)
    ax_cost = fig.add_subplot (212)

    ax_data.plot (data, 'b', lw=1)
    ax_data.axvline (opt.x, color='k', lw=2)
    ax_data.set_ylabel ('data')

    ax_cost.plot (scores-data.min (), 'r', lw=2)
    ax_cost.set_ylabel ('cost')
    ax_cost.set_xlabel ('cost')

    plt.show ()
    sys.exit (0)
