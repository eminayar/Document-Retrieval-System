import os
import re
import json

#open files
reuters_dir = os.path.abspath(os.path.join( os.getcwd() , '../reuters21578'))
punctuations_file = open( os.path.abspath(os.path.join( os.getcwd() , '../punctuations.txt')) , "r" )
stopwords_file = open( os.path.abspath(os.path.join( os.getcwd() , '../stopwords.txt')) , "r" )
index_file = open( os.path.abspath(os.path.join( os.getcwd() , '../Output/index.json')) , "w" )
bigram_file = open( os.path.abspath(os.path.join( os.getcwd() , '../Output/bigrams.json')) , "w" )


#some statistics
num_tokens_before_stopwords = 0
num_tokens_after_stopwords = 0
unique_tokens_before_cf = set()
unique_tokens_after_stopword = set()
frequency_before = {}
frequency_after = {}

def tokenize( input ):
    global num_tokens_before_stopwords
    global num_tokens_after_stopwords
    #clear punctuations
    input = input.strip()
    without_punc = ""
    for char in input:
        if char in punctuations:
            without_punc += ' '
        else:
            without_punc += char

    #some statistics
    for tkn in without_punc.split():
        unique_tokens_before_cf.add(tkn)
        if tkn in frequency_before:
            frequency_before[tkn] += 1
        else:
            frequency_before[tkn] = 1

    #case folding
    tokens = list(map( lambda x: x.lower(), without_punc.split() ))
    num_tokens_before_stopwords += len(tokens)
    #stopword removal
    tokens = list(filter( lambda x: x not in stopwords , tokens ))
    #for the report
    num_tokens_after_stopwords += len(tokens)
    for tkn in tokens:
        unique_tokens_after_stopword.add(tkn)
        if tkn in frequency_after:
            frequency_after[tkn] += 1
        else:
            frequency_after[tkn] = 1
    return tokens

index = {}
bigrams = {}

def parse( filename ):
    file_dir = os.path.join( reuters_dir , filename )
    f = open(file_dir , encoding='latin1').read()
    #split documents using REUTERS tag
    all_documents = re.findall('<REUTERS.*?</REUTERS>',f, flags = re.DOTALL)
    for document in all_documents:
        #get document id
        doc_id = int(re.search('NEWID=.*?>',document).group(0).split('"')[1].split('"')[0])
        #get title and body
        title = re.search('<TITLE>.*?</TITLE>',document, flags = re.DOTALL)
        if title:
            title = title.group(0).split("<TITLE>")[1].split("</TITLE>")[0]
        else:
            title = ""
        body = re.search('<BODY>.*?&#3;</BODY>',document, flags = re.DOTALL)
        if body:
            body = body.group(0).split("<BODY>")[1].split("&#3;</BODY>")[0]
        else:
            body = ""
        #get tokens
        tokens = tokenize( title ) + tokenize( body )
        #puts tokens into index
        for token in tokens:
            if not token in index:
                index[token] = [doc_id]
            elif index[token][-1] != doc_id:
                index[token].append(doc_id)

#read punctuations
punctuations = set()
for punc in punctuations_file:
    punctuations.add(r"{}".format(str(punc).strip()))

#read stopwords
stopwords = set()
for word in stopwords_file:
    stopwords.add(r"{}".format(str(word).strip()))

for filename in os.listdir(reuters_dir):
    if ".sgm" in filename:
        parse(filename)

#for bigrams
json.dump(index, index_file , sort_keys=True )
for i in sorted(index):
    key = "$"+i+"$"
    for j in range( len(key)-1 ):
        bi = key[j:j+2]
        if not bi in bigrams:
            bigrams[bi] = [i]
        elif bigrams[bi][-1] != i:
            bigrams[bi].append( i )

json.dump(bigrams , bigram_file , sort_keys=True )
##some statistics
print("num_tokens_before_stopwords: "+str(num_tokens_before_stopwords))
print("num_tokens_after_stopwords: "+str(num_tokens_after_stopwords))
print("num_unique_tokens_before_cf: "+str(len(unique_tokens_before_cf)))
print("num_unique_tokens_after_stopword: "+str(len(unique_tokens_after_stopword)))
current = 0
terms = []
for term in sorted(frequency_before.items(), key = lambda x:x[1], reverse=True):
    terms.append(term[0])
    current += 1
    if current == 20:
        break
current = 0
print("top20-before:"+str(terms))
terms = []
for term in sorted(frequency_after.items(), key = lambda x:x[1], reverse=True):
    terms.append(term[0])
    current += 1
    if current == 20:
        break
print("top20-after:"+str(terms))
