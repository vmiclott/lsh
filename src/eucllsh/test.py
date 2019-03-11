import time

import numpy as np

from src.eucllsh.p2lsh import *

p2Lsh = P2LSH()

r = 10
l = 20
k = 2
d = 10
n = 1000
data = 100 * np.random.random((n, d))
# np.save('data',data)
# data = np.load('data.npy')
p = 100 * np.random.random(d)
# np.save('p',p)
# p = np.load('p.npy')
currentTime = time.time()
functions = p2Lsh.makeHashFunctions(d, l, k, r)
# p1Lsh.saveHashFunctions(functions, 'hashFunction')
# functions = p1Lsh.loadHashFunctions(l, 'hashFunction')
functionDict = p2Lsh.hashData(data, functions)
time0 = time.time() - currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = p2Lsh.nearNeighbor(p, data, functionDict, functions)
time1 = time.time() - currentTime
currentTime = time.time()
nearestNeighbor = p2Lsh.nearestNeighbor(p, data)
time2 = time.time() - currentTime
# print("Query")
# print(p)
print("Near Neighbor (index): " + str(neighbor))
# print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(p2Lsh.dist(p, data[neighbor])))
print("Nearest Neighbor (index):" + str(nearestNeighbor))
# print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(p2Lsh.dist(p, data[nearestNeighbor])))
