from scipy.cluster.vq import kmeans
import numpy as np

from src.LSH import LSH


class KMeansHashFunction:
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
        np.savetxt(fileName, self.centroids)


class KLSH(LSH):
    def dist(self, a, b):
        return np.linalg.norm(np.subtract(a, b))

    def saveHashFunctions(self, functions, fileName):
        if fileName.endswith('.txt'):
            fileName.replace('.txt', '')
        for i in range(len(functions)):
            name = fileName + str(i) + '.txt'
            functions[i].save(name)

    def loadHashFunctions(self, l, fileName):
        functions = []
        for i in range(l):
            name = fileName + str(i) + '.txt'
            centroids = np.loadtxt(name)
            k = len(centroids)
            functions.append(KMeansHashFunction(k, None, centroids))
        return functions

    # Construct l hash functions for d-dimensional points in Hamming space
    def makeHashFunctions(self, l, k, train):
        functions = []
        for i in range(l):
            functions.append(KMeansHashFunction(k, train))
        return functions

