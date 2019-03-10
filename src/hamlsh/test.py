import time

import numpy as np

from src.hamlsh.hamlsh import *

hammLsh = HammingLSH()

l = 15
k = 25
d = 50
n = 10000
data = np.random.randint(0, 2, (n, d))
np.save('data',data)
#data = np.load('data.npy')
p = np.random.randint(0, 2, d)
np.save('p',p)
#p = np.load('p.npy')

currentTime = time.time()
functions = hammLsh.makeHashFunctions(d, l, k)
# hammLsh.saveHashFunctions(functions, 'hashFunction')
# functions = hammLsh.loadHashFunctions(l, 'hashFunction')
functionDict = hammLsh.hashData(data, functions)
time0 = time.time() - currentTime
print("Preprocessing time: " + str(time0))
currentTime = time.time()
neighbor = hammLsh.nearNeighbor(p, data, functionDict, functions)
time1 = time.time() - currentTime
currentTime = time.time()
nearestNeighbor = hammLsh.nearestNeighbor(p, data)
time2 = time.time() - currentTime
# print("Query")
# print(p)
print("Near Neighbor (index): " + str(neighbor))
# print(data[neighbor])
print("Time: " + str(time1))
print("Distance to query: " + str(hammLsh.dist(p, data[neighbor])))
print("Nearest Neighbor (index)" + str(nearestNeighbor))
# print(data[nearestNeighbor])
print("Time: " + str(time2))
print("Distance to query: " + str(hammLsh.dist(p, data[nearestNeighbor])))