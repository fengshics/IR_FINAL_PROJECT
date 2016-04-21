import nltk
import os

HTML_DOCUMENT_PATH = 'cacm/'
RELEVANT_DOCUMENTS_SCORE_LIST_FILE_NAME = 'BM25.txt'
EXPANDED_QUERIES_FILE_NAME = 'expanded_queries_by_prf.txt'
RELEVANT_TOP_DOCUMENTS_K = '10'
RELEVANT_TOP_TERMS_K = '20'

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


def retrieveTopKDocsForQueries():
	topKDocsForQueriesDict = {}
	with open(RELEVANT_DOCUMENTS_SCORE_LIST_FILE_NAME, 'r') as f:
		for docRecord in f:



def expandQueries():
