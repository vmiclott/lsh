import numpy as np


class LSH:
    def dist(self, a, b):
        pass

    # Hash all n points from a d-dimensional data set in Hamming space, returns the buckets containing indices of points
    def hashDataWithFunction(self, data, function):
        hashDict = {}
        for i in range(len(data)):
            hashcode = function.hash(data[i])
            if hashcode in hashDict.keys():
                hashDict[hashcode].add(i)
            else:
                hashDict[hashcode] = {i}
        return hashDict

    def hashData(self, data, functions):
        functionDict = {}
        for i in range(len(functions)):
            functionDict[i] = self.hashDataWithFunction(data, functions[i])
        return functionDict

    def saveFunctionDict(self, functionDict, fileName):
        for i in range(len(functionDict)):
            name = fileName + str(i)
            np.save(name, functionDict[i])

    def loadFunctionDict(self, l, fileName):
        functionDict = {}
        for i in range(l):
            name = fileName + str(i) + '.npy'
            functionDict[i] = np.load(name).item()
        return functionDict

    # Find near neighbor using hash codes
    def nearNeighbor(self, p, data, functionDict, functions):
        indices = set()
        for i in range(len(functions)):
            hashcode = functions[i].hash(p)
            hashDict = functionDict[i]
            if hashcode in hashDict.keys():
                indices.update(hashDict[hashcode])
        print("Items in same bucket (amount): " + str(len(indices)))
        print("Items in same bucket (indices): " + str(indices))
        minDist = 0
        nearNeighbor = None
        for index in indices:
            dist = self.dist(p, data[index])
            if nearNeighbor is None:
                nearNeighbor = index
                minDist = dist
            elif dist < minDist:
                nearNeighbor = index
                minDist = dist
            if minDist == 0:
                return nearNeighbor
        return nearNeighbor

    def nearestNeighbor(self, p, data):
        minDist = 0
        nearestNeighbor = None
        for index in range(len(data)):
            dist = self.dist(p, data[index])
            if nearestNeighbor is None:
                nearestNeighbor = index
                minDist = dist
            elif dist < minDist:
                nearestNeighbor = index
                minDist = dist
            if minDist == 0:
                return nearestNeighbor
        return nearestNeighbor
