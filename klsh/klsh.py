import sys
from scipy.cluster.vq import kmeans
from lsh.util import dotdict
import numpy as np

#Cluster data using kmeans and euclidean distance.
def cluster(data,k):
    centroids, distortion = kmeans(data,k)
    return centroids

#Make l*k buckets defined by the k centroids of l iterations of kmeans with different seeds.
def makeBuckets(train, l, k):
    allBuckets = {}
    for i in range(l):
        buckets = {}
        centroids = cluster(train, k)
        for j in range(k):
            buckets[j] = centroids[j]
        allBuckets[i] = buckets
    return allBuckets

#Hash a datapoint to a l buckets by finding the buckets with closest centroid in each of the l collections of buckets.
def hash(p,buckets):
    hashcodes = []
    for i in range(len(buckets)):
        mindist = float('inf')
        hashcode = (-1,-1)
        b = buckets[i]
        for j in range(len(b)):
            c = b[j]
            dist = np.linalg.norm(np.subtract(p,c))
            if dist < mindist:
                hashcode = (i,j)
                mindist = dist
        hashcodes.append(hashcode)
    return hashcodes

#Hash a whole dataset using given buckets.
def hashData(data, buckets, l, k):
    hashDict = {}
    for i in range(l):
        for j in range(k):
            hashDict[(i,j)] = []
    for i in range(len(data)):
        hashCodes = hash(data[i], buckets)
        for h in hashCodes:
            hashDict[h].append(i)
    return hashDict

#Parse command line arguments.
def parsecl(argv):
    settings = {}
    settings['data'] = ''
    settings['train'] = ''
    settings['buckets'] = ''
    settings['centroids'] = ''
    settings['k'] = -1
    settings['l'] = -1
    settings = dotdict(settings)
    for i in range(len(argv)):
        flag = argv[i][0:2]
        val = argv[i][2:]
        if flag == '-d':
            settings.data = np.load(val)
        if flag == '-t':
            settings.train = np.load(val)
        if flag == '-b':
            settings.buckets = val
        if flag == '-c':
            settings.centroids = val
        if flag == '-k':
            settings.k = int(val)
        if flag == '-l':
            settings.l = int(val)
    return settings

def main(argv):
    settings = parsecl(argv)
    print('Hashing data to ' + str(settings.k*settings.l) + ' buckets.')
    buckets = makeBuckets(settings.train, settings.l, settings.k)
    hashDict = hashData(settings.data,buckets,settings.l,settings.k)
    file = open(settings.buckets,'w')
    for code in hashDict.keys():
        file.write(str(code[0]) + ' ' + str(code[1]))
        file.write('\n')
        for index in hashDict[code]:
            file.write(str(index) + ' ')
        file.write('\n')
    file.close()
    file = open(settings.centroids, 'w')
    for i in range(len(buckets)):
        b = buckets[i]
        for j in range(len(b)):
            c = b[j]
            file.write(str(i) + ' ' + str(j))
            file.write('\n')
            file.write(str(c))
            file.write('\n')
    file.close()

if __name__ == "__main__":
    main(sys.argv)