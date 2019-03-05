import numpy as np
import time


class HashFunction:
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
            self.seed = np.random.randint(0,2147483647)
        np.random.seed(self.seed)
        self.a = np.random.standard_cauchy((k, d))
        self.b = np.random.randint(0, r, k)

    def hash(self, p):
        hashcode = np.zeros(self.k)
        for i in range(self.k):
            hashcode[i] = np.floor((np.matmul(self.a[i], p) + self.b[i]) / self.r)
        return tuple(hashcode)

    def save(self, fileName):
        f = open(fileName, 'w')
        f.write('dimension ' + str(d) + '\n')
        f.write('k ' + str(k) + '\n')
        f.write('r ' + str(r) + '\n')
        f.write('seed ' + str(self.seed))


def manhDist(a, b):
    return sum(np.absolute(a - b))


def saveHashFunctions(functions, fileName):
    if fileName.endswith('.txt'):
        fileName.replace('.txt','')
    for i in range(len(functions)):
        name = fileName + str(i) + '.txt'
        functions[i].save(name)


def loadHashFunctions(fileName, l):
    functions = []
    for i in range(l):
        name = fileName+str(i)+'.txt'
        f = open(name, 'r')
        d = f.readline().split(' ')[1]
        k = f.readline().split(' ')[1]
        r = f.readline().split(' ')[1]
        seed = f.readline().split(' ')[1]
        functions.append(HashFunction(d,k,r,seed))
    return functions


# Construct l hash functions for d-dimensional points in Hamming space
def makeHashFunctions(d, l, k, r):
    functions = []
    for i in range(l):
        functions.append(HashFunction(d, k, r))
    return functions


# Hash all n points from a d-dimensional data set in Hamming space, returns the buckets containing indices of points
def hashDataWithFunction(data, function):
    hashDict = {}
    for i in range(len(data)):
        hashcode = function.hash(data[i])
        if hashcode in hashDict.keys():
            hashDict[hashcode].add(i)
        else:
            hashDict[hashcode] = {i}
    return hashDict


def hashData(data, functions):
    functionDict = {}
    for i in range(len(functions)):
        functionDict[i] = hashDataWithFunction(data, functions[i])
    return functionDict


# Find near neighbor using hash codes
def nearNeighbor(p, data, functionDict, functions):
    indices = set()
    for i in range(len(functions)):
        hashcode = functions[i].hash(p)
        hashDict = functionDict[i]
        if hashcode in hashDict.keys():
            indices.update(hashDict[hashcode])
    minDist = 0
    nearNeighbor = None
    for index in indices:
        dist = manhDist(p, data[index])
        if nearNeighbor is None:
            nearNeighbor = index
            minDist = dist
        elif dist < minDist:
            nearNeighbor = index
            minDist = dist
        if minDist == 0:
            return nearNeighbor
    return nearNeighbor


def nearestNeighbor(p, data):
    minDist = 0
    nearestNeighbor = None
    for index in range(len(data)):
        dist = manhDist(p, data[index])
        if nearestNeighbor is None:
            nearestNeighbor = index
            minDist = dist
        elif dist < minDist:
            nearestNeighbor = index
            minDist = dist
        if minDist == 0:
            return nearestNeighbor
    return nearestNeighbor


r = 10
l = 20
k = 2
d = 10
n = 1000
#data = np.random.randint(0, 10, (n, d))
#p = np.random.randint(0, 10, d)
#np.save('data',data)
#np.save('p',p)
data = np.load('data.npy')
p = np.load('p.npy')
currentTime = time.time()
#functions = makeHashFunctions(d, l, k, r)
functions = loadHashFunctions('hashFunction',20)
saveHashFunctions(functions,'hashFunction')
functionDict = hashData(data, functions)
time0 = time.time() - currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = nearNeighbor(p, data, functionDict, functions)
time1 = time.time() - currentTime
currentTime = time.time()
nearestNeighbor = nearestNeighbor(p, data)
time2 = time.time() - currentTime
# print("Query")
# print(p)
print("Near Neighbor (index): " + str(neighbor))
# print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(manhDist(p, data[neighbor])))
print("Nearest Neighbor (index)" + str(nearestNeighbor))
# print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(manhDist(p, data[nearestNeighbor])))
