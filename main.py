import os
import shutil
import sys
import time

from src.hamlsh.hamlsh import *
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


def main(argv):
    settings = parsecl(argv)
    if settings.method == 'hamlsh':
        doHamLsh(settings)


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

        currentTime = time.time()
        functions = lsh.makeHashFunctions(d, l, k)
        functionDict = lsh.hashData(data, functions)
        baseDir = os.path.dirname(settings.f)
        if os.path.isdir(baseDir):
            shutil.rmtree(baseDir)
        os.makedirs(baseDir)
        lsh.saveHashFunctions(functions, f)
        lsh.saveFunctionDict(functionDict, h)
        time0 = time.time() - currentTime
        print("Preprocessing time: " + str(time0))
    if not settings.preprocess:
        p = settings.query
        data = settings.data
        functions = lsh.loadHashFunctions(settings.l, settings.functions)
        functionDict = lsh.loadFunctionDict(settings.l, settings.functionDict)
        currentTime = time.time()
        neighbor = lsh.nearNeighbor(p, data, functionDict, functions)
        time1 = time.time() - currentTime
        currentTime = time.time()
        nearestNeighbor = lsh.nearestNeighbor(p, data)
        time2 = time.time() - currentTime
        # print("Query")
        # print(p)
        print("Near Neighbor (index): " + str(neighbor))
        # print(data[neighbor])
        print("Time: " + str(time1))
        print("Distance to query: " + str(lsh.dist(p, data[neighbor])))
        print("Nearest Neighbor (index):" + str(nearestNeighbor))
        # print(data[nearestNeighbor])
        print("Time: " + str(time2))
        print("Distance to query: " + str(lsh.dist(p, data[nearestNeighbor])))


if __name__ == "__main__":
    main(sys.argv[1:])
