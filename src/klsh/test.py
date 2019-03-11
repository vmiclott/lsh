import time

import numpy as np

from src.klsh.klsh import *

kLsh = KLSH()

l = 20
k = 10
d = 10
n = 1000
data = np.random.random_sample((n, d))
# np.save('data',data)
# data = np.load('data.npy')
p = np.random.random_sample(d)
# np.save('p',p)
# p = np.load('p.npy')
train = data[0:100]
# np.save('train',train)
# train = np.load('train.npy')
functions = kLsh.makeHashFunctions(l, k, train)
# kLsh.saveHashFunctions(functions, 'hashFunction')
# functions = kLsh.loadHashFunctions(l, 'hashFunction')
functionDict = kLsh.hashData(data, functions)

currentTime = time.time()
time0 = time.time() - currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = kLsh.nearNeighbor(p, data, functionDict, functions)
time1 = time.time() - currentTime
currentTime = time.time()
nearestNeighbor = kLsh.nearestNeighbor(p, data)
time2 = time.time() - currentTime
print("Query")
print(p)
print("Near Neighbor (index): " + str(neighbor))
print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(kLsh.dist(p, data[neighbor])))
print("Nearest Neighbor (index)" + str(nearestNeighbor))
print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(kLsh.dist(p, data[nearestNeighbor])))
