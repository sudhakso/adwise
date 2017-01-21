'''
Created on Jan 15, 2017

@author: sonu
'''
import re
import nltk
from nltk.classify import *


class ClassifierHelper:
    def __init__(self, featureListFile, stopwordsFile):
        self.wordFeatures = []
        # Read feature list
        inpfile = open(featureListFile, 'r')
        line = inpfile.readline()
        while line:
            self.wordFeatures.append(line.strip())
            line = inpfile.readline()
        # Read Stop words file
        self.stopfile = stopwordsFile
        self.stopwords = self._getStopWordList(self.stopfile)

    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.wordFeatures:
            word = self.replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            features['contains(%s)' % word] = (word in document_words)
        return features

    def replaceTwoOrMore(self, s):
        # pattern to look for three or more repetitions of any character,
        # including newlines.
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def _getStopWordList(self, stopWordListFileName):
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')
        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords

    def getFeatureVector(self, tweet):
        featureVector = []
        words = tweet.split()
        for w in words:
            # replace two or more with two occurrences
            w = self.replaceTwoOrMore(w)
            # strip punctuation
            w = w.strip('\'"?,.')
            # check if it consists of only words
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
            # ignore if it is a stopWord
            if(w in self.stopwords or val is None):
                continue
            else:
                featureVector.append(w.lower())
        return featureVector

    # start process_tweet
    def process_tweet(self, tweet):
        # Convert to lower case
        tweet = tweet.lower()
        # Convert https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',
                       'URL',
                       tweet)
        # Convert @username to AT_USER
        tweet = re.sub('@[^\s]+',
                       'AT_USER',
                       tweet)
        # Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        # Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        # trim
        tweet = tweet.strip()
        # remove first/last " or 'at string end
        tweet = tweet.rstrip('\'"')
        tweet = tweet.lstrip('\'"')
        return tweet
    # end

    # start is_ascii
    def is_ascii(self, word):
        return all(ord(c) < 128 for c in word)
    # end
