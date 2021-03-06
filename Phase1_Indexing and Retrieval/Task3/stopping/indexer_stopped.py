import nltk
import os
from bs4 import BeautifulSoup
import string

HTML_DOCUMENT_PATH = '../../../Given_Corpus_Info/cacm/'
INDEX_FILE_NAME = 'unigram_index_stopped.txt'
DOCUMENT_LENGTH_PATH = 'document_length_stopped.txt'
COMMON_WORDS_FILENAME = '../../../Given_Corpus_Info/common_words.txt'

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

def indexer(path):
    unigram = {}
    fw = open(DOCUMENT_LENGTH_PATH, 'w')
    n = 0
    N = 0
    for fileName in os.listdir(path):
        if fileName == '.DS_Store':
            continue
        f = open(path + fileName, 'r')
        # retrieve document name
        documentName = fileName[0: fileName.find('.html')]
        # tokenize
        tokens = tokenize(f.read())
        tokens = removeStoppingWords(tokens)
        # document length
        n += len(tokens)
        N += 1
        fw.write(documentName + ' ' + str(len(tokens)) + '\n')

        termFrequencies = nltk.FreqDist(tokens)
        for term, tf in termFrequencies.iteritems():
            if term in unigram:
                unigram[term].append( (documentName, tf) )
            else:
                unigram[term] = [ (documentName, tf) ]
        f.close()
    #fw.write(str(n) + ' ' + str(N) + ' ' + str(n / N) + '\n')
    fw.write(str(n / N) + '\n')
    fw.close()
    writeInFile(unigram)

def writeInFile(unigram):
    f = open(INDEX_FILE_NAME, 'w')
    for key in sorted(unigram):
            f.write(key + " ")
            value = unigram[key]
            for documentId, tf in value:
                f.write(documentId + ":" + str(tf) + " ")
            f.write("\n")
    f.close()

if __name__ == '__main__':
    '''
    sentence = """At eight o'clock on Thursday morning "2.434", 345, 345, 234,345, (asdfasdf)."""
    tokens = nltk.word_tokenize(sentence)
    tokens = filter(lambda a: a != '``', tokens)
    tokens = filter(lambda a: a != "''", tokens)
    for token in tokens:
        print token + '\n'
    '''
    indexer(HTML_DOCUMENT_PATH)

    pass