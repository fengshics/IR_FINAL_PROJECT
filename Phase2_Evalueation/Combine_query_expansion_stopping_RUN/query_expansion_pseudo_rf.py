import nltk
import os
from bs4 import BeautifulSoup
import string
import math

HTML_DOCUMENT_PATH = '../../Given_Corpus_Info/cacm/'
RELEVANT_DOCUMENTS_SCORE_LIST_FILE_NAME = 'BM25_with_rel_stopping.txt'
ORIGINAL_QUERIES_FILE_NAME = 'cacm_query_tokens_stopped.txt'
EXPANDED_QUERIES_FILE_NAME = 'expanded_queries_by_prf_stopped.txt'
COMMON_WORDS_FILENAME = '../../Given_Corpus_Info/common_words.txt'
RELEVANT_TOP_DOCUMENTS_K = 5
RELEVANT_TOP_TERMS_K = 10


def tokenize(rawHtml):
    soup = BeautifulSoup(rawHtml, 'html.parser')
    rawDocument = soup.getText().encode('utf-8').lower()
    tokens = nltk.word_tokenize(rawDocument)
    for punctuation in string.punctuation:
        tokens = filter(lambda a: a != punctuation, tokens)
    # remove `` manually
    tokens = filter(lambda a: a != "``", tokens)
    # remove '' manually
    tokens = filter(lambda a: a != "''", tokens)
    return tokens

def retrieveCommonWords():
    stopWordsList = []
    with open(COMMON_WORDS_FILENAME, 'r') as f:
        for stopRecord in f:
            if stopRecord == '\n':
                continue
            stopWordsList.append(stopRecord.strip())

    return stopWordsList


def removeStoppingWords(tokens):
    stopWordsList = retrieveCommonWords()
    tokens = filter(lambda a: a not in stopWordsList, tokens)
    return tokens

def retrieveOriginalQueryTokens():
	originalQueryTokensList = []
	with open(ORIGINAL_QUERIES_FILE_NAME, 'r') as f:
		for queryRecord in f:
			if queryRecord == '\n':
				continue
			queryRecord = queryRecord.strip()
			originalQueryTokensList.append(queryRecord)

	return originalQueryTokensList

def retrieveTopKDocsForQueries():
	topKDocsForQueriesDict = {}
	recordArray = []
	with open(RELEVANT_DOCUMENTS_SCORE_LIST_FILE_NAME, 'r') as f:
		for docRecord in f:
			if docRecord == '\n':
				continue
			recordArray = docRecord.split(' ')
			queryId = int(recordArray[0])
			docId = recordArray[2]
			rank = int(recordArray[3])
			if rank > RELEVANT_TOP_DOCUMENTS_K:
				continue
			if topKDocsForQueriesDict.has_key(queryId):
				topKDocsForQueriesDict[queryId].append(docId)
			else:
				topKDocsForQueriesDict[queryId] = [docId]
	return topKDocsForQueriesDict

def retrieveTokensFromDocsList(docList):
	tokens = []
	for docId in docList:
		with open(HTML_DOCUMENT_PATH + docId + '.html', 'r') as f:
			tokens += tokenize(f.read())
	return tokens

def calculateTermScore(frequency, n, N):
    tf = frequency
    idf = math.log(N / (n * 1.0), 10)
    return tf * idf

def indexDocuments(docList):
	tokens = []
	index = {}
	for docId in docList:
		with open(HTML_DOCUMENT_PATH + docId + '.html', 'r') as f:
			tokens = tokenize(f.read())
			tokens = removeStoppingWords(tokens)
			termFrequencies = nltk.FreqDist(tokens)
			for term, tf in termFrequencies.iteritems():
				if term.isdigit():
					continue 
				if term in index:
					index[term].append( (docId, tf) )
				else:
					index[term] = [ (docId, tf) ]

	return index

def getTopKExpandWordsForQueryTFIDF(docList):
	N = len(docList)
	index = indexDocuments(docList)
	tfIdfScoreDict = {}
	for term, invertedlist in index.iteritems():
		frequency = 0
		for docId, tf in invertedlist:
			frequency += tf
		tfIdfScore = calculateTermScore(frequency, len(invertedlist), N)
		tfIdfScoreDict[term] = tfIdfScore
	sortedTFIDFList = sorted(tfIdfScoreDict.items(), key=lambda t: t[1], reverse = True)
	topKList = getTopKFromList(sortedTFIDFList, RELEVANT_TOP_TERMS_K)
	return topKList

def getTopKExpandWordsForQueryTF(docList):
	tokens = retrieveTokensFromDocsList(docList)
	termFrequencies = nltk.FreqDist(tokens)
	sortedTermFrequencies = sorted(termFrequencies.items(), key=lambda t: t[1], reverse = True)
	topKList = getTopKFromList(sortedTermFrequencies, RELEVANT_TOP_TERMS_K)
	return topKList

def getTopKFromList(tList, k):
	count = 0
	topKList = []
	for e, tf in tList:
		count += 1
		if count > k:
			break
		topKList.append(e)

	return topKList


def expandQueries():
	topKDocsForQueriesDict = retrieveTopKDocsForQueries()
	originalQueryTokensList = retrieveOriginalQueryTokens()
	print str(len(originalQueryTokensList))
	for queryId, docList in topKDocsForQueriesDict.iteritems():
		#print 'expand query ' + str(queryId)
		topKWordsList = getTopKExpandWordsForQueryTFIDF(docList)
		originalQueryTokensList[queryId - 1] = originalQueryTokensList[queryId - 1] + \
		' ' + ' '.join(topKWordsList)
	saveExpandedQueries(originalQueryTokensList)
	
def saveExpandedQueries(expandedQueriesList):
	f = open(EXPANDED_QUERIES_FILE_NAME, 'w')
	for expandedQuery in expandedQueriesList:
		f.write(expandedQuery + '\n')
	f.close()


if __name__ == '__main__':
	expandQueries()
	



