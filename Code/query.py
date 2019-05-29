import sys
import os
import json

operation = int(sys.argv[1])
query = sys.argv[2]

index_file = open( os.path.abspath(os.path.join( os.getcwd() , '../Output/index.json')) , "r" )
index = json.load(index_file)
bigram_file = open( os.path.abspath(os.path.join( os.getcwd() , '../Output/bigrams.json')) , "r" )
bigrams = json.load(bigram_file)

#get intersection of two lists
def intersection(lst1, lst2):
    lst3 = list(filter(lambda x: x in lst1, lst2))
    return lst3

#get union of two lists
def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

#postfilter's filter
def possible(original, test):
    left = original.split('*')[0]
    right = original.split('*')[1]
    return test.startswith(left) and test.endswith(right)

#type1 query handler
def type1query(query):
    keywords = list(map(lambda x: x.strip().lower() , query.split(" AND ")))
    for keyword in keywords:
        if keyword not in index:
            return []
    keywords.sort(key= lambda x: len(index[x]))
    ret = index[keywords[0]]
    for i in range(1,len(keywords)):
        ret = intersection(ret, index[keywords[i]])
    return ret

#type2 query handler
def type2query(query):
    keywords = list(map(lambda x: x.strip().lower() , query.split(" OR ")))
    ret = []
    for keyword in keywords:
        if keyword in index:
            ret = union(ret , index[keyword])
    return ret

#type3 query handler
def type3query(query):
    query = query.lower()
    original = query
    query = "$" + query.split('*')[0] + query.split('*')[1] + "$"
    indexes = []
    for i in range(len(query)-1):
        bi = query[i:i+2]
        if bi in bigrams:
            indexes = union( bigrams[bi] , indexes )

    indexes = list(filter(lambda x: possible(original, x), indexes))
    indexes.sort()
    if len(indexes) == 0:
        return []
    new_query = indexes[0]
    for i in range( 1 , len(indexes) ):
        new_query += " OR "+indexes[i]
    print(new_query)
    return type2query(new_query)

if operation == 1:
    answer = type1query(query)
elif operation == 2:
    answer = type2query(query)
elif operation == 3:
    answer = type3query(query)

print(sorted(answer))
