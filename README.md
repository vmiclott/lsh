# Theory:
During preprocessing, every data point from a data set is hashed using `l` hash functions in such a way that close points `(dist <R)` are hashed to the same bucket with chance `p1` and far points `(dist > cR)` are hashed to the same bucket with chance `p2` for each hash function.  
  
A given query will be hashed using the same `l` hash functions and will be compared to (currently all) `3l` data points from its buckets to find the nearest neighbor (this should be a near neighbor in the whole data set).

# General Usage:
`python main.py`  
```
Arguments for preprocessing:
  argument        required/optional                   default value                 description    
  -p              required                                                          enable preprocessing
  -m<method>      required                                                          lsh method can be either of hamlsh, p1lsh, p2lsh, klsh
  -D<data.npy>    required                                                          path to data set (numpy array with rows being the data points)
  -R<val>         required for hamlsh, p1lsh, p2lsh                                 R radius of ball around query that contains at least 1 data point
  -c<val>         required for hamlsh, p1lsh, p2lsh                                 approx. factor for ANN
  -T<train.npy>   required for klsh                                                 training set (usually subset of data.npy) to train kmeans
  -l<val>         required for klsh                                                 amount of clusterings to be made
  -k<val>         required for klsh                                                 amount of centroids per clustering
  [-f<save>]      optional                            resources/hashFunc            path to save hash functions
  [-h<save>]      optional                            resources/hashCodesForFunc    path to save hashcodes for each hash function
  [-o<save>]      optional                            output/output.txt             path to save output file with running information
```
```
Arguments for LSH:
  argument        required/optional   default value                 description
  -m<method>      required                                          lsh method can be either of hamlsh, p1lsh, p2lsh, klsh
  -D<data.npy>    required                                          path to data set (numpy array with rows being the data points)
  -Q<query.npy>   required                                          path to query (numpy array)
  -l<val>         required                                          amount of hashfunctions
  [-f<save>]      optional            resources/hashFunc            path to load hash functions from
  [-h<save>]      optional            resources/hashCodesForFunc    path to load hashcodes for each hash function from
  [-o<save>]      optional            output/output.txt             path to save output file with running information
```

# HamLSH Example: 

Data properties:  
n = 10000  
d = 50  
data = randomBinary((n,d))  
queries = randomBinary((1000,d))  

`...\lsh>python main.py -p -mhamlsh -Ddata/data.npy -R15 -c2 -fsave/savedHashFunction -hsave/savedHashCodes -oout/preprocess`  
#### out/preprocess.txt:
p1: 0.7  
p2: 0.4  
rho: 0.3892595783536952  
R: 15.0  
c: 2.0  
l: 36  
k: 10  
n: 10000  
d: 50  
Preprocessing time: 3.2562215328216553  

`...\lsh>python main.py -mhamlsh -Ddata/data.npy -Qdata/queries.npy -l36 -fsave/savedHashFunction -hsave/savedHashCodes -oout/results`  
#### out/results.txt
Number of queries: 1000  
Accuracy: 0.975  
Time (LSH): 1.1503241062164307  
Time (Linear Scan): 11.678465366363525  
Near neighbors (LSH):  
[6304, 7333, 46, ..., 2509]  
Nearest neighbors (Linear Scan):  
[836, 7333, 46, ..., 2509]  
Distances:  
[13, 12, 12, ..., 10]  
Exact Distances:  
[13, 12, 12, ..., 10]  
