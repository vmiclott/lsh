import numpy as np
class Lsh:

    def __init__(self, method, n, d, l, k):
        self.method = method
        self.n = n
        self.d = d
        self.l = l
        self.k = k
        self.hashfunctions = None
        self.data = None
        self.trainingData = None
        self.hashDict = None

    def hash(self, p):
        hashcodes = np.empty((self.l, self.k + 1), dtype=int)
        for i in range(self.l):
            hashcodes[i, 0] = i
            for j in range(self.k):
                index = self.hashfunctions[i, j]
                hashcodes[i, j + 1] = p[index]
        return hashcodes
