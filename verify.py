# Author: Wennan Zhu
# Maximum weight matching, verify lower bound example

import random
import math
import numpy as np
from scipy.optimize import linprog
import itertools
import copy
import json
import time

class Bipartite(object):
    def __init__(self, n, m, filename):
        self.n = n # size of bipartite graph
        self.m = m # sampling number for RSD
        # distance matrix for bipartite graph
        with open(filename) as f:
            self.d = json.load(f)
        self.lp_result = 0
        self.rsd_result = 0

    def get_result(self):
        return self.lp_result/self.rsd_result

    # LP solver
    def lp(self):
        n = self.n
        d_temp = np.negative(np.array(self.d)) # use minimize solver, negative c
        c = d_temp.reshape(n*n).tolist()
        b = [1 for i in range(2 * n)]
        bounds = tuple([(0, None) for i in range(n * n)])
        A = [[0 for i in range(n * n)] for j in range(2 * n)]

        # sum of x_ij = 1 for all i, and for all j
        for i in range(n):
            for j in range(n):
                A[i][i * n + j] = 1
        for j in range(n):
            for i in range(n):
                A[n + j][i * n + j] = 1

        res = linprog(c, A_eq=A, b_eq=b, bounds=bounds, options={"disp": True, "maxiter": 5000})
        self.lp_result = -res.fun

    # RSD solver
    def RSD(self):
        n = self.n
        #generate preference profile
        p = []
        for i in range(n):
            pref = np.argsort(self.d[i])
            p.append(pref[::-1])

        total_value = 0
        for count in range(self.m):
            # biparite graph: only consider the right hand side: 1 stands for available, 0 stands for taken
            r = [1 for j in range(n)]

            # Random permutation
            order = np.random.permutation(n)
            #result = []
            result_value = 0
            for i in order:
                # get i's most prefered available item in b
                k = 0
                while r[p[i][k]] == 0:
                    k += 1
                    continue
                r[p[i][k]] = 0
                #result.append((i, p[i][k]))
                result_value += self.d[i][p[i][k]]
            total_value += result_value
        self.rsd_result = total_value/self.m

def main():
    start = time.time()
    # Run RSD sampling for m times
    m = 100000
    # n: size of the bipartite graph
    n = 50
    bipartite = Bipartite(n, m, 'example_50.txt')
    bipartite.lp()
    bipartite.RSD()
    print bipartite.get_result()
    end = time.time()
    print "Running time: " + str(end - start)

if __name__ == "__main__":
    main()
