import numpy as np
import time


class HashFunction:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.indices = np.random.randint(0, d, k)

    def hash(self, p):
        return tuple(p[self.indices])


# Construct l hash functions for d-dimensional points in Hamming space
def makeHashFunctions(d, l, k):
    functions = set()
    for i in range(l):
        functions.add(HashFunction(d, k))
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


def hashData(data,functions):
    functionDict = {}
    for function in functions:
        functionDict[function] = hashDataWithFunction(data, function)
    return functionDict


# Find near neighbor using hash codes
def nearNeighbor(p, data, functionDict, functions):
    indices = set()
    for function in functions:
        hashcode = function.hash(p)
        hashDict = functionDict[function]
        if hashcode in hashDict.keys():
            indices.update(hashDict[hashcode])
    minDist = 0
    nearNeighbor = None
    for index in indices:
        dist = np.count_nonzero(p != data[index])
        if nearNeighbor is None:
            nearNeighbor = index
            minDist = dist
        elif dist < minDist:
            nearNeighbor = index
            minDist = dist
        if minDist == 0:
            return nearNeighbor
    return nearNeighbor


def nearestNeighbor(p,data):
    minDist = 0
    nearestNeighbor = None
    for index in range(len(data)):
        dist = np.count_nonzero(p != data[index])
        if nearestNeighbor is None:
            nearestNeighbor = index
            minDist = dist
        elif dist < minDist:
            nearestNeighbor = index
            minDist = dist
        if minDist == 0:
            return nearestNeighbor
    return nearestNeighbor

l = 20
k = 20
d = 1000
n = 1000000
data = np.random.randint(0,2,(n,d))
p = np.random.randint(0,2,d)

currentTime = time.time()
functions = makeHashFunctions(d,l,k)
functionDict = hashData(data,functions)
time0 = time.time()-currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = nearNeighbor(p,data,functionDict,functions)
time1 = time.time()-currentTime
currentTime = time.time()
nearestNeighbor = nearestNeighbor(p,data)
time2 = time.time()-currentTime
#print("Query")
#print(p)
print("Near Neighbor (index): " + str(neighbor))
#print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(np.count_nonzero(p != data[neighbor])))
print("Nearest Neighbor (index)" + str(nearestNeighbor))
#print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(np.count_nonzero(p != data[nearestNeighbor])))