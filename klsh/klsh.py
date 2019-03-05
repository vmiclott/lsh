from scipy.cluster.vq import kmeans
import numpy as np
import time

class HashFunction:
    def __init__(self, k, train=None, centroids=None):
        k = int(k)
        self.k = k
        if centroids is not None:
            self.centroids = centroids
        elif train is not None:
            self.centroids, self.distortion = kmeans(train, k)

    def hash(self, p):
        minDist = float('inf')
        hashcode = np.zeros(self.k)
        for i in range(self.k):
            centroid = self.centroids[i]
            dist = np.linalg.norm(np.subtract(p, centroid))
            if dist < minDist:
                minDist = dist
                hashcode = centroid
        return tuple(hashcode)


    def save(self, fileName):
        np.savetxt(fileName,self.centroids)



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
        centroids = np.loadtxt(name)
        k = len(centroids)
        functions.append(HashFunction(k,None,centroids))
    return functions


# Construct l hash functions for d-dimensional points in Hamming space
def makeHashFunctions(l, k, train):
    functions = []
    for i in range(l):
        functions.append(HashFunction(k, train))
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
        dist = np.linalg.norm(np.subtract(p, data[index]))
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
        dist = np.linalg.norm(np.subtract(p, data[index]))
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
data = np.random.random_sample((n, d))
p = np.random.random_sample(d)
train = data[0:100]
functions = makeHashFunctions(l,k,train)
functionDict = hashData(data, functions)

currentTime = time.time()
time0 = time.time() - currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = nearNeighbor(p, data, functionDict, functions)
time1 = time.time() - currentTime
currentTime = time.time()
nearestNeighbor = nearestNeighbor(p, data)
time2 = time.time() - currentTime
print("Query")
print(p)
print("Near Neighbor (index): " + str(neighbor))
print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(np.linalg.norm(np.subtract(p, data[neighbor]))))
print("Nearest Neighbor (index)" + str(nearestNeighbor))
print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(np.linalg.norm(np.subtract(p, data[nearestNeighbor]))))