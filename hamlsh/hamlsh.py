import numpy as np


# Constructs l*k hash functions for d-dimensional points in Hamming space
def makeHashFunctions(d,l,k):
    functions = np.empty((l,k),dtype=int)
    for i in range(l):
        for j in range(k):
            index = np.random.randint(0,d)
            functions[i,j] = index
    return functions

# Hashes a d-dimensional point in Hamming space using the l*k hash functions constructed through makeHashFunctions
def hash(p,functions,l,k):
    hashcodes = np.empty((l,k),dtype=int)
    for i in range(l):
        for j in range(k):
            index = functions[i,j]
            hashcodes[i,j] = p[index]
    return hashcodes

# Hashes all n points from a d-dimensional data set in Hamming space, returns the buckets containing indices of points
def hashData(data,functions,l,k):
    hashDict = {}
    n = len(data)
    for i in range(n):
        hashcodes = hash(data[i],functions,l,k)
        for j in range(l):
            hashcode = (j,) + tuple(hashcodes[j])
            if hashcode in hashDict.keys():
                hashDict[hashcode].append(i)
            else:
                hashDict[hashcode] = [i]
    return hashDict
