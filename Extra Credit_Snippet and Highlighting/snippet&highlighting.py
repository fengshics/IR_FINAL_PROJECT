__author__ = 'Vigery'

import os
from bs4 import BeautifulSoup
import string
import nltk
import math

INDEXPATH = "../Given_Corpus_Info/unigram.txt"
RETRIEVAL_MODELS_PATH = '../All Runs Ranking Results/'
HTML_PATH = '../Given_Corpus_Info/cacm/'
RESULT_PATH = 'Snippet and Highlighting Result/'
QUERY_FILE_NAME = 'cacm_query_token.txt'

N = 3204

index = {}
nDictionary = {}
queries = {}

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
    f.close()

def parseQueryText(queryText):
    queryDictionary = {}
    for queryTerm in queryText.split(" "):
        if queryTerm in queryDictionary:
            queryDictionary[queryTerm] += 1
        else:
            queryDictionary[queryTerm] = 1
    return queryDictionary

def getSnippet(rawSnippet):
    s = []
    for i in range(20):
        if i == 19:
            s.append(rawSnippet[i])
        else:
            s.append(rawSnippet[i])
            s.append(' ')
    snippet = ''.join(s)
    '''
    for i in range(20):
        if i == 19:
            snippet += rawSnippet[i]
        else:
            snippet += rawSnippet[i] + ' '
    '''
    return snippet

def tokenize(snippet):
    tokens = nltk.word_tokenize(snippet)
    for punctuation in string.punctuation:
        tokens = filter(lambda a: a != punctuation, tokens)
    # remove `` manually
    tokens = filter(lambda a: a != "``", tokens)
    # remove '' manually
    tokens = filter(lambda a: a != "''", tokens)
    return tokens

def calculateScore(tokens, queryDictionary):
    score = 0
    for token in tokens:
        if token in queryDictionary:
            invertedList = index[token]
            n = len(invertedList)
            idf = math.log(N / (n * 1.0), 10)
            score += idf
    return score

def findHighlights(tokens, queryDictionary):
    highlights = []
    for i in range(len(tokens)):
        token = tokens[i]
        if token in queryDictionary:
            highlights.append(i)
    return highlights

def findSnippet(queryText, rawDocument, fw):
    bestSnippet = ''
    bestSnippetScore = 0
    queryDictionary = parseQueryText(queryText)
    rawDocument = rawDocument.replace('\n', ' ')
    rawDocumentToken = rawDocument.split(' ')
    rawDocumentToken = filter(None, rawDocumentToken)
    snippets = nltk.ngrams(rawDocumentToken, 20)
    for rawSnippet in snippets:
        snippet = getSnippet(rawSnippet)
        tokens = tokenize(snippet.lower())
        score = calculateScore(tokens, queryDictionary)
        if score > bestSnippetScore:
            bestSnippetScore = score
            bestSnippet = snippet
    fw.write('Snippet: ' + bestSnippet + '\n')
    # highlighting
    fw.write('Highlight words: ')
    words = tokenize(bestSnippet)
    for word in words:
        if word.lower() in queryDictionary:
            fw.write(word + ' ')
    fw.write('\n')

def snippetAndHighlighting(path):
    for fileName in os.listdir(path):
        if fileName == '.DS_Store':
            continue

        with open(RESULT_PATH + 'snippet_and_highlighting_' + fileName, 'w') as fw:
            # read query results from previous file
            with open(path + fileName, 'r') as fr:
                for queryResult in fr:
                    fw.write(queryResult)
                    items = queryResult.split(' ')
                    queryID = items[0]
                    documentID = items[2]
                    htmlName = documentID + '.html'
                    with open(HTML_PATH + htmlName, 'r') as fhtml:
                        rawHtml = fhtml.read()
                        soup = BeautifulSoup(rawHtml, 'html.parser')
                        rawDocument = soup.getText().encode('utf-8')
                        query = queries[queryID]
                        query = query[0: query.find('\n') - 1]
                        findSnippet(query, rawDocument, fw)
            fr.close()
        fw.close()

def retrieveQueries(fileName):
    with open(fileName, 'r') as f:
        queryID = 0
        for query in f:
            queryID += 1
            queries[str(queryID)] = query
    f.close()

if __name__ == '__main__':

    # read index from previous file
    retrieveIndex()

    # read query tokens from previous file
    retrieveQueries(QUERY_FILE_NAME)

    snippetAndHighlighting(RETRIEVAL_MODELS_PATH)

    pass