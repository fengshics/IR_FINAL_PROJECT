__author__ = 'Vigery'


INDEXPATH = "unigram.txt"
DOCUMENTLENGTHPATH = "document length.txt"
QUERY_FILE_PATH = "cacm_query_token.txt"

N = 3204

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


if __name__ == '__main__':

    # read index from previous file
    retrieveIndex()
    # read document length information from previous file
    #retrieveDocumentLength()
    # do the query
    queryID = 0

    file = open("BM25.txt", "w")
    with open(QUERY_FILE_PATH, "r") as f:
        for query in f:
            query = query[0: query.find('\n') - 1]
            queryID += 1
            doQuery(queryID, query, file)
    file.close()
    pass