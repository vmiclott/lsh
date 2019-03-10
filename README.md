# HamLSH: 
Preprocessing arguments: -mhamlsh -p -Ddataset.npy -Rval -cval [-fsaveHashFunctions -hsaveHashCodes]
Output:
k = ...
l = ...
Preprocessing time = ...

ANN vs NN arguments: -mhamlsh -Ddataset.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]
Output:
Items in same buckets (indices): {...}
ANN (index): ...
Time: ...
Distance to query: ...
NN (index): ...
Time: ...
Distance to query: ...

### EXAMPLE (https://puu.sh/CXStY.png):

Data properties:
n = 10000
d = 50
data = randomBinary((n,d))
p = randomBinary(d)


...\lsh>python main.py -p -mhamlsh -Dhamdata/data.npy -R15 -c2 -fhamsave/savedHashFunction -hhamsave/savedHashCodes
l: 36
k: 10
Preprocessing time: 4.428683280944824

...\lsh>python main.py -mhamlsh -Dhamdata/data.npy -Qhamdata/p.npy -l36 -fhamsave/savedHashFunction -hhamsave/savedHashCodes
Items in same bucket (indices): {4097, 7172, 9223, 3079, ..., 9213, 8191}
Near Neighbor (index): 6564
Time: 0.003987550735473633
Distance to query: 11
Nearest Neighbor (index):6564
Time: 0.02393817901611328
Distance to query: 11

# P1LSH:
Preprocessing arguments: -mp1lsh -p -Ddataset.npy -Rval -cval [-fsaveHashFunctions -hsaveHashCodes]
Output:
k = ...
l = ...
Preprocessing time = ...

ANN vs NN arguments: -mp1lsh -Ddataset.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]
Output:
Items in same buckets (indices): {...}
ANN (index): ...
Time: ...
Distance to query: ...
NN (index): ...
Time: ...
Distance to query: ...


### EXAMPLE (https://puu.sh/CXTcl.png):

Data properties:
n = 10000
d = 20
data = normal(0,1,(n,d))
p = normal(0,1,d)


...\lsh>python main.py -p -mp1lsh -Dp1data/data.npy -R15 -c2 -fp1save/savedHashFunction -hp1save/savedHashCodes
l: 249
k: 11
Preprocessing time: 277.0569860935211

...\lsh>python main.py -mp1lsh -Dp1data/data.npy -Qp1data/p.npy -l249 -fp1save/savedHashFunction -hp1save/savedHashCodes
Items in same bucket (indices): {2, 4101, 8198, 7, ..., 6141, 6142}
Near Neighbor (index): 4668
Time: 0.02889871597290039
Distance to query: 13.977791704736852
Nearest Neighbor (index):4668
Time: 0.06685209274291992
Distance to query: 13.977791704736852
