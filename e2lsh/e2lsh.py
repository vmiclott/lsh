import numpy as np

d = 3
v = np.random.normal(10, 5, d)
a = np.random.normal(0, 1, d)
print(a)
print(v)
print(np.matmul(a, v))


def makeHashFunctions(d, l, k, r):
    allFunctions = {}
    for i in range(l):
        allFunctions[i] = []
        for j in range(k):
            a = np.random.normal(0, 1, d)
            b = np.random.uniform(0, r)
            allFunctions[i].append(a, b)
    return allFunctions


def hash(p, functions, r):
    hashcodes = []
    for key in functions.keys:
        hashcode = ()
        for function in functions[key]:
            a = function[0]
            b = function[0]
            hashcode += np.floor((np.matmul(a, p) + b) / r)
        hashcodes.append(hashcode)
    return hashcodes


def hashData(data, functions, r, l, k):
    hashDict = {}
    for i in range(len(data)):
        hashCodes = hash(data[i], functions)
        for h in hashCodes:
            hashDict[h].append(i)
    return hashDict



def hashData(data, buckets, l):
    hashDict = {}
    for i in range(l):
        for j in range(k):
            hashDict[(i, j)] = []
    for i in range(len(data)):
        hashCodes = hash(data[i], buckets)
        for h in hashCodes:
            hashDict[h].append(i)
    return hashDict
