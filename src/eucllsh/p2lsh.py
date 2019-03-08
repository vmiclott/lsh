import numpy as np

from src.LSH import LSH


class P2HashFunction:
    def __init__(self, d, k, r, seed=None):
        d = int(d)
        k = int(k)
        r = int(r)
        self.d = d
        self.k = k
        self.r = r
        if seed:
            self.seed = int(seed)
        else:
            self.seed = np.random.randint(0, 2147483647)
        np.random.seed(self.seed)
        self.a = np.random.normal(0, 1, (k, d))
        self.b = np.random.randint(0, r, k)

    def hash(self, p):
        hashcode = np.zeros(self.k)
        for i in range(self.k):
            hashcode[i] = np.floor((np.matmul(self.a[i], p) + self.b[i]) / self.r)
        return tuple(hashcode)

    def save(self, fileName):
        f = open(fileName, 'w')
        f.write('dimension ' + str(self.d) + '\n')
        f.write('k ' + str(self.k) + '\n')
        f.write('r ' + str(self.r) + '\n')
        f.write('seed ' + str(self.seed))


class P2LSH(LSH):
    def dist(self, a, b):
        return np.linalg.norm(np.subtract(a, b))

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
            r = f.readline().split(' ')[1]
            seed = f.readline().split(' ')[1]
            functions.append(P2HashFunction(d, k, r, seed))
        return functions

    # Construct l hash functions for d-dimensional points in Hamming space
    def makeHashFunctions(self, d, l, k, r):
        functions = []
        for i in range(l):
            functions.append(P2HashFunction(d, k, r))
        return functions
