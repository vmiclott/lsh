import os
import shutil
import sys
import time
import math

from src.hamlsh.hamlsh import *
from src.eucllsh.p2lsh import *
from src.manhlsh.p1lsh import *
from src.klsh.klsh import *
from src.util import dotdict


def parsecl(argv):
    """Parse command line arguments."""
    settings = {}
    settings = dotdict(settings)
    settings.method = None
    settings.functions = None
    settings.preprocess = False
    settings.output = 'output/output.txt'
    settings.h = 'resources/hashCodesForFunc'
    settings.f = 'resources/hashFunc'
    settings.functionDict = 'resources/hashCodesForFunc'
    settings.functions = 'resources/hashFunc'
    for i in range(len(argv)):
        flag = argv[i][0:2]
        val = argv[i][2:]
        if flag == '-p':
            settings.preprocess = True
        if flag == '-m':
            settings.method = val
        if flag == '-l':
            settings.l = int(val)
        if flag == '-k':
            settings.k = int(val)
        if flag == '-R':
            settings.R = float(val)
        if flag == '-c':
            settings.c = float(val)
        if flag == '-D':
            settings.data = np.load(val)
        if flag == '-T':
            settings.train = np.load(val)
        if flag == '-F':
            settings.functions = val
        if flag == '-f':
            settings.f = val
        if flag == '-H':
            settings.functionDict = val
        if flag == '-h':
            settings.h = val
        if flag == '-Q':
            settings.query = np.load(val)
        if flag == '-o':
            settings.output = val
    return settings


def doP1Lsh(settings):
    lsh = P1LSH()
    if settings.preprocess:
        if settings.method is None or settings.data is None or settings.R is None or settings.c is None: return
        data = settings.data
        f = settings.f
        h = settings.h
        n = len(data)
        d = len(data[0])
        R = settings.R
        r = 4 * R
        c = settings.c
        p1 = 2 / math.pi * math.atan(r / R) - R / (math.pi * r) * np.log((r / R) ** 2 + 1)
        p2 = 2 / math.pi * math.atan(r / (c * R)) - (c * R) / (math.pi * r) * np.log((r / (c * R)) ** 2 + 1)
        rho = np.log(1 / p1) / np.log(1 / p2)
        l = int(np.power(n, rho))
        k = int(np.log(n) / np.log(1 / p2))
        print('l: ' + str(l))
        print('k: ' + str(k))
        print('n: ' + str(n))
        print('d: ' + str(d))
        currentTime = time.time()
        functions = lsh.makeHashFunctions(d, l, k, r)
        functionDict = lsh.hashData(data, functions)
        baseDir = os.path.dirname(f)
        if os.path.isdir(baseDir):
            shutil.rmtree(baseDir)
        if baseDir != '':
            os.makedirs(baseDir)
        lsh.saveHashFunctions(functions, f)
        lsh.saveFunctionDict(functionDict, h)
        time0 = time.time() - currentTime
        print("Preprocessing time: " + str(time0))
    if not settings.preprocess:
        p = settings.query
        data = settings.data
        f = settings.f
        h = settings.h
        l = settings.l
        functions = lsh.loadHashFunctions(l, f)
        functionDict = lsh.loadFunctionDict(l, h)
        currentTime = time.time()
        neighbor = lsh.nearNeighbor(p, data, functionDict, functions)
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbor = lsh.nearestNeighbor(p, data)
        time2 = time.time() - currentTime
        print("Near Neighbor (index): " + str(neighbor))
        print("Time: " + str(time1))
        print("Distance to query: " + str(lsh.dist(p, data[neighbor])))
        print("Nearest Neighbor (index):" + str(nearestNeighbor))
        print("Time: " + str(time2))
        print("Distance to query: " + str(lsh.dist(p, data[nearestNeighbor])))


def doP2Lsh(settings):
    lsh = P2LSH()
    if settings.preprocess:
        if settings.method is None or settings.data is None or settings.R is None or settings.c is None: return
        data = settings.data
        f = settings.f
        h = settings.h
        n = len(data)
        d = len(data[0])
        R = settings.R
        r = 4 * R
        c = settings.c
        p1 = 1 - (1 + math.erf(-r / (R * math.sqrt(2)))) - (2 * R) / (math.sqrt(2 * math.pi) * r) * (
            1 - math.exp(-r ** 2 / (2 * R ** 2)))
        p2 = 1 - (1 + math.erf(-r / ((c * R) * math.sqrt(2)))) - (2 * (c * R)) / (math.sqrt(2 * math.pi) * r) * (
            1 - math.exp(-r ** 2 / (2 * (c * R) ** 2)))
        rho = np.log(1 / p1) / np.log(1 / p2)
        l = int(np.power(n, rho))
        k = int(np.log(n) / np.log(1 / p2))
        print('l: ' + str(l))
        print('k: ' + str(k))
        currentTime = time.time()
        functions = lsh.makeHashFunctions(d, l, k, r)
        functionDict = lsh.hashData(data, functions)
        baseDir = os.path.dirname(f)
        if os.path.isdir(baseDir):
            shutil.rmtree(baseDir)
        if baseDir != '':
            os.makedirs(baseDir)
        lsh.saveHashFunctions(functions, f)
        lsh.saveFunctionDict(functionDict, h)
        time0 = time.time() - currentTime
        print("Preprocessing time: " + str(time0))
    if not settings.preprocess:
        p = settings.query
        data = settings.data
        f = settings.f
        h = settings.h
        l = settings.l
        functions = lsh.loadHashFunctions(l, f)
        functionDict = lsh.loadFunctionDict(l, h)
        currentTime = time.time()
        neighbor = lsh.nearNeighbor(p, data, functionDict, functions)
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbor = lsh.nearestNeighbor(p, data)
        time2 = time.time() - currentTime
        print("Near Neighbor (index): " + str(neighbor))
        print("Time: " + str(time1))
        print("Distance to query: " + str(lsh.dist(p, data[neighbor])))
        print("Nearest Neighbor (index):" + str(nearestNeighbor))
        print("Time: " + str(time2))
        print("Distance to query: " + str(lsh.dist(p, data[nearestNeighbor])))


def doKLsh(settings):
    lsh = KLSH()
    if settings.preprocess:
        if settings.method is None or settings.data is None or settings.train is None: return
        train = settings.train
        data = settings.data
        f = settings.f
        h = settings.h
        n = len(data)
        d = len(data[0])
        R = settings.R
        c = settings.c
        l = settings.l
        k = settings.k
        print('l: ' + str(l))
        print('k: ' + str(k))
        print('n: ' + str(n))
        print('d: ' + str(d))
        currentTime = time.time()
        functions = lsh.makeHashFunctions(l, k, train)
        functionDict = lsh.hashData(data, functions)
        baseDir = os.path.dirname(f)
        if os.path.isdir(baseDir):
            shutil.rmtree(baseDir)
        if baseDir != '':
            os.makedirs(baseDir)
        lsh.saveHashFunctions(functions, f)
        lsh.saveFunctionDict(functionDict, h)
        time0 = time.time() - currentTime
        print("Preprocessing time: " + str(time0))
    if not settings.preprocess:
        p = settings.query
        data = settings.data
        f = settings.f
        h = settings.h
        l = settings.l
        functions = lsh.loadHashFunctions(l, f)
        functionDict = lsh.loadFunctionDict(l, h)
        currentTime = time.time()
        neighbor = lsh.nearNeighbor(p, data, functionDict, functions)
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbor = lsh.nearestNeighbor(p, data)
        time2 = time.time() - currentTime
        print("Near Neighbor (index): " + str(neighbor))
        print("Time: " + str(time1))
        print("Distance to query: " + str(lsh.dist(p, data[neighbor])))
        print("Nearest Neighbor (index):" + str(nearestNeighbor))
        print("Time: " + str(time2))
        print("Distance to query: " + str(lsh.dist(p, data[nearestNeighbor])))


def doHamLsh(settings):
    lsh = HammingLSH()
    if settings.preprocess:
        if settings.method is None or settings.data is None or settings.R is None or settings.c is None: return
        data = settings.data
        f = settings.f
        h = settings.h
        n = len(data)
        d = len(data[0])
        R = settings.R
        c = settings.c
        p1 = 1 - R / d
        p2 = 1 - c * R / d
        rho = np.log(1 / p1) / np.log(1 / p2)
        l = int(np.power(n, rho))
        k = int(np.log(n) / np.log(1 / p2))
        print('l: ' + str(l))
        print('k: ' + str(k))
        print('n: ' + str(n))
        print('d: ' + str(d))
        currentTime = time.time()
        functions = lsh.makeHashFunctions(d, l, k)
        functionDict = lsh.hashData(data, functions)
        baseDir = os.path.dirname(f)
        if os.path.isdir(baseDir):
            shutil.rmtree(baseDir)
        if baseDir != '':
            os.makedirs(baseDir)
        lsh.saveHashFunctions(functions, f)
        lsh.saveFunctionDict(functionDict, h)
        time0 = time.time() - currentTime
        print("Preprocessing time: " + str(time0))
    '''
    if not settings.preprocess:
        p = settings.query
        data = settings.data
        f = settings.f
        h = settings.h
        l = settings.l
        functions = lsh.loadHashFunctions(l, f)
        functionDict = lsh.loadFunctionDict(l, h)
        currentTime = time.time()
        neighbor = lsh.nearNeighbor(p, data, functionDict, functions)
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbor = lsh.nearestNeighbor(p, data)
        time2 = time.time() - currentTime
        print("Near Neighbor (index): " + str(neighbor))
        print("Time: " + str(time1))
        print("Distance to query: " + str(lsh.dist(p, data[neighbor])))
        print("Nearest Neighbor (index):" + str(nearestNeighbor))
        print("Time: " + str(time2))
        print("Distance to query: " + str(lsh.dist(p, data[nearestNeighbor])))
    '''
    if not settings.preprocess:
        queries = settings.query
        data = settings.data
        f = settings.f
        h = settings.h
        l = settings.l
        functions = lsh.loadHashFunctions(l, f)
        functionDict = lsh.loadFunctionDict(l, h)
        currentTime = time.time()
        nearNeighbors = []
        for p in queries:
            nearNeighbors.append(lsh.nearNeighbor(p, data, functionDict, functions))
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbors = []
        for p in queries:
            nearestNeighbors.append(lsh.nearestNeighbor(p, data))
        time2 = time.time() - currentTime
        accuracy = 0
        for i in range(len(queries)):
            if lsh.dist(queries[i], data[nearNeighbors[i]])==lsh.dist(queries[i], data[nearestNeighbors[i]]):
                accuracy += 1
        print("Number of queries: " + str(len(queries)))
        print("Accuracy: " + str(accuracy/len(queries)))
        print("Time (LSH): " + str(time1))
        print("Time (Brute Force): " + str(time2))


def main(argv):
    settings = parsecl(argv)
    if settings.method == 'hamlsh':
        doHamLsh(settings)
    if settings.method == 'p1lsh':
        doP1Lsh(settings)
    if settings.method == 'p2lsh':
        doP2Lsh(settings)
    if settings.method == 'klsh':
        doKLsh(settings)


if __name__ == "__main__":
    main(sys.argv[1:])
