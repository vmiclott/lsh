# General Usage:
`python main.py`  
```
Arguments for preprocessing:
  -p            required                            enable preprocessing
  -mmethod      required                            lsh method can be either of hamlsh, p1lsh, p2lsh, klsh
  -Ddata.npy    required                            path to data set
  -Rval         required for hamlsh, p1lsh, p2lsh   R radius of ball around query that contains at least 1 data point
  -cval         required for hamlsh, p1lsh, p2lsh   approx. factor for ANN
  -Ttrain.npy   required for klsh                   training set (usually subset of data.npy) to train kmeans
  -lval         required for klsh                   amount of clusterings to be made
  -kval         required for klsh                   amount of centroids per clustering
  [-fsave]      optional                            path to save hash functions
  [-hsave]      optional                            path to save hashcodes for each hash function
```
```
Arguments for LSH:
  -mmethod      required                            lsh method can be either of hamlsh, p1lsh, p2lsh, klsh
  -Ddata.npy    required                            path to data set
  -Qquery.npy   required                            path to query
  -lval         required                            amount of hashfunctions
  [-fsave]      optional                            path to load hash functions from
  [-hsave]      optional                            path to load hashcodes for each hash function from
```

# HamLSH: 
Preprocessing arguments: `-p -mhamlsh -Ddata.npy -Rval -cval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
k = ...  
l = ...  
Preprocessing time = ...  

ANN vs NN arguments: `-mhamlsh -Ddata.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]`  
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


`...\lsh>python main.py -p -mhamlsh -Dhamdata/data.npy -R15 -c2 -fhamsave/savedHashFunction -hhamsave/savedHashCodes`  
l: 36  
k: 10  
Preprocessing time: 4.428683280944824  

`...\lsh>python main.py -mhamlsh -Dhamdata/data.npy -Qhamdata/p.npy -l36 -fhamsave/savedHashFunction -hhamsave/savedHashCodes`  
Items in same bucket (indices): {4097, 7172, 9223, 3079, ..., 9213, 8191}  
Near Neighbor (index): 6564  
Time: 0.003987550735473633  
Distance to query: 11  
Nearest Neighbor (index):6564  
Time: 0.02393817901611328  
Distance to query: 11  

# P1LSH:
Preprocessing arguments: `-p -mp1lsh -Ddata.npy -Rval -cval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
k = ...  
l = ...  
Preprocessing time = ...  

ANN vs NN arguments: `-mp1lsh -Ddata.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]`  
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


`...\lsh>python main.py -p -mp1lsh -Dp1data/data.npy -R15 -c2 -fp1save/savedHashFunction -hp1save/savedHashCodes`  
l: 249  
k: 11  
Preprocessing time: 277.0569860935211  

`...\lsh>python main.py -mp1lsh -Dp1data/data.npy -Qp1data/p.npy -l249 -fp1save/savedHashFunction -hp1save/savedHashCodes`  
Items in same bucket (indices): {2, 4101, 8198, 7, ..., 6141, 6142}  
Near Neighbor (index): 4668  
Time: 0.02889871597290039  
Distance to query: 13.977791704736852  
Nearest Neighbor (index):4668  
Time: 0.06685209274291992  
Distance to query: 13.977791704736852  


# P2LSH:
Preprocessing arguments: `-p -mp2lsh -Ddata.npy -Rval -cval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
k = ...  
l = ...  
Preprocessing time = ...  

ANN vs NN arguments: `-mp2lsh -Ddata.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
Items in same buckets (indices): {...}  
ANN (index): ...  
Time: ...  
Distance to query: ...  
NN (index): ...  
Time: ...  
Distance to query: ...  


### EXAMPLE:

Data properties:  
n = 10000  
d = 20  
data = normal(0,1,(n,d))  
p = normal(0,1,d)  

`...\lsh>python main.py -p -mp2lsh -Dp2data/data.npy -R5 -c2 -fp2save/savedHashFunction -hp2save/savedHashCodes`  
l: 62  
k: 18  
Preprocessing time: 78.0030996799469  

`...\lsh>python main.py -mp2lsh -Dp2data/data.npy -Qp2data/p.npy -l62 -fp2save/savedHashFunction -hp2save/savedHashCodes`  
Items in same bucket (indices): {0, 8194, 8198, 4103, ..., 8186, 4095}  
Near Neighbor (index): 4668  
Time: 0.03188443183898926  
Distance to query: 4.04929771735058  
Nearest Neighbor (index):4668  
Time: 0.06981325149536133  
Distance to query: 4.04929771735058  

# KLSH:
Preprocessing arguments: `-p -mklsh -Ddata.npy -Ttrain.npy -lval -kval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
k = ...  
l = ...  
Preprocessing time = ...  

ANN vs NN arguments: `-mklsh -Ddata.npy -Qquery.npy -lval [-fsaveHashFunctions -hsaveHashCodes]`  
Output:  
Items in same buckets (indices): {...}  
ANN (index): ...  
Time: ...  
Distance to query: ...  
NN (index): ...  
Time: ...  
Distance to query: ...  


### EXAMPLE (https://puu.sh/CXTSt.png):

Data properties:  
n = 10000  
d = 20  
data = 10 gaussian clusters centers (0,0,...,0), (1,1,...,1), ..., (9,9,...,9) with sigma 1  
trainindices = random(0,n,n/100)  
train = data[trainindices]  
p = normal(0,1,d)  

`...\lsh>python main.py -p -mklsh -Dkdata/data.npy -Tkdata/train.npy -l20 -k20 -fksave/savedHashFunction -hksave/savedHashCodes`  
l: 20  
k: 20  
Preprocessing time: 30.465436458587646  

`...\lsh>python main.py -mklsh -Dkdata/data.npy -Qkdata/p.npy -l20 -fksave/savedHashFunction -hksave/savedHashCodes`  
Items in same bucket (indices): {0, 1, 2, 3, ..., 1947, 1954}  
Near Neighbor (index): 680  
Time: 0.01992034912109375  
Distance to query: 3.8583251886429895  
Nearest Neighbor (index):680  
Time: 0.0628666877746582  
Distance to query: 3.8583251886429895  
