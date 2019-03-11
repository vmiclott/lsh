import numpy as np

from src.LSH import LSH


class HammingHashFunction:
    def __init__(self, d, k, seed=None):
        d = int(d)
        k = int(k)
        self.d = d
        self.k = k
        if seed:
            self.seed = int(seed)
        else:
            self.seed = np.random.randint(0, 2147483647)
        np.random.seed(self.seed)
        self.indices = np.random.randint(0, d, k)

    def hash(self, p):
        return tuple(p[self.indices])

    def save(self, fileName):
        f = open(fileName, 'w')
        f.write('dimension ' + str(self.d) + '\n')
        f.write('k ' + str(self.k) + '\n')
        f.write('seed ' + str(self.seed))


class HammingLSH(LSH):
    def dist(self, a, b):
        return np.count_nonzero(a != b)

    def saveHashFunctions(self, functions, fileName):
        if fileName.endswith('.txt'):
            fileName.replace('.txt', '')
        for i in range(len(functions)):
            name = fileName + str(i) + '.txt'
            functions[i].save(name)

    def loadHashFunctions(self, l, fileName):
        functions = []
        for i in range(l):
            name = fileName + str(i) + '.txt'
            f = open(name, 'r')
            d = f.readline().split(' ')[1]
            k = f.readline().split(' ')[1]
            seed = f.readline().split(' ')[1]
            functions.append(HammingHashFunction(d, k, seed))
        return functions

    # Construct l hash functions for d-dimensional points in Hamming space
    def makeHashFunctions(self, d, l, k):
        functions = []
        for i in range(l):
            functions.append(HammingHashFunction(d, k))
        return functions
