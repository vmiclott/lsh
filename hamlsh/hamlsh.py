import numpy as np


# Construct l*k hash functions for d-dimensional points in Hamming space
def makeHashFunctions(d,l,k):
    functions = np.empty((l,k),dtype=int)
    for i in range(l):
        for j in range(k):
            index = np.random.randint(0,d)
            functions[i,j] = index
    return functions

# Hash a d-dimensional point in Hamming space using the l*k hash functions constructed through makeHashFunctions
def hash(p,functions,l,k):
    hashcodes = np.empty((l,k+1),dtype=int)
    for i in range(l):
        hashcodes[i,0] = i
        for j in range(k):
            index = functions[i,j]
            hashcodes[i,j+1] = p[index]
    return hashcodes

# Hash all n points from a d-dimensional data set in Hamming space, returns the buckets containing indices of points
def hashData(data,functions,l,k):
    hashDict = {}
    n = len(data)
    for i in range(n):
        hashcodes = hash(data[i],functions,l,k)
        for j in range(l):
            hashcode = tuple(hashcodes[j])
            if hashcode in hashDict.keys():
                hashDict[hashcode].append(i)
            else:
                hashDict[hashcode] = [i]
    return hashDict

# Find near neighbor using hash codes
def nearNeighbor(p,data,hashDict,functions,l,k):
    hashcodes = hash(p,functions,l,k)
    indices = set()
    for i in range(l):
        hashcode = tuple(hashcodes[i])
        if hashcode in hashDict:
            indices.update(hashDict[hashcode])
    minDist = 0
    nearNeighbor = None
    for index in indices:
        dist = np.count_nonzero(p!=data[index])
        if nearNeighbor is None:
            nearNeighbor = index
            minDist = dist
        elif dist < minDist:
            nearNeighbor = index
            minDist = dist
        if minDist == 0:
            return nearNeighbor
    return nearNeighbor