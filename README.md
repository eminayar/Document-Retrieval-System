# Document-Retrieval-System
Document retrieval system for simple boolean and wildcard queries using the bigram indexing scheme

Reuters-21578 dataset is used.

* (type1 query) w1 AND w2 AND w3... AND wn
* (type2 query) w1 OR w2 OR w3... OR wn
* (type3 query) w∗

usage: python query.py \<query type\> \<query\>

for example: python process.py 1 "people AND car"
