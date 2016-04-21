__author__ = 'Vigery'

import math
import operator

INDEXPATH = "unigram.txt"
DOCUMENTLENGTHPATH = "document length.txt"
QUERY_FILE_PATH = "cacm_query_token.txt"

k1 = 1.2
b = 0.75
k2 = 100
N = 3204
avg = 0

index = {}
documentLength = {}
nDictionary = {}

def retrieveIndex():
    with open(INDEXPATH, "r") as f:
        for invertedList in f:
            space = invertedList.find(" ")
            term = invertedList[0:space]
            tfs = invertedList[space + 1:]
            documentList = []
            b = tfs.split(" ")
            n = 0
            for tf in b:
                if tf == "\n":
                    continue
                a = tf.split(":")
                documentID = a[0]
                frequency = int(a[1])
                item = ( documentID, frequency )
                n += 1
                documentList.append(item)
            index[term] = documentList
            nDictionary[term] = n

def retrieveDocumentLength():
    global avg
    file = open(DOCUMENTLENGTHPATH, "r")
    for i in range(N):
        s = file.readline().split(" ")
        documentLength[s[0]] = int(s[1])
    s = file.readline()
    avg = int(s)
    file.close()

def parseQueryText(queryText):
    queryDictionary = {}
    for queryTerm in queryText.split(" "):
        if queryTerm in queryDictionary:
            queryDictionary[queryTerm] += 1
        else:
            queryDictionary[queryTerm] = 1
    return queryDictionary

def calculateTermScore(documentID, f, qf, term):
    k = k1 * ((1 - b) + b * documentLength[documentID] / avg)
    ni = nDictionary[term]
    beforeLog = (N - ni) / (ni * 1.0) * (k1 + 1) * f / ((k + f) * 1.0) * (k2 + 1) * qf / ((k2 + qf) * 1.0)
    score = math.log(beforeLog)
    return score

def doQuery(queryID, queryText, file):
    BM25 = {}
    queryDictionary = parseQueryText(queryText)
    for queryTerm in queryDictionary:
        if queryTerm in index:
            invertedList = index[queryTerm]
        else:
            continue
        for documentID, frequency in invertedList:
            termScore = calculateTermScore(documentID, frequency, queryDictionary[queryTerm], queryTerm)
            if documentID in BM25:
                BM25[documentID] += termScore
            else:
                BM25[documentID] = termScore
    sorted_scores = sorted(BM25.items(), key=operator.itemgetter(1), reverse=True)
    rank = 1
    for documentID, score in sorted_scores:
        queryID = '0' + str(queryID) if queryID < 10 else str(queryID)
        file.write(queryID + " Q0 " + documentID + " " + str(rank) + " " + str(score) + " BM25\n")
        rank += 1
        if rank == 101:
            break

if __name__ == '__main__':

    # read index from previous file
    retrieveIndex()
    # read document length information from previous file
    retrieveDocumentLength()
    # do the query
    queryID = 0

    file = open("BM25.txt", "w")
    with open(QUERY_FILE_PATH, "r") as f:
        for query in f:
            query = query[0: query.find('\n') - 1]
            print query
            queryID += 1
            doQuery(queryID, query, file)
    file.close()
    pass