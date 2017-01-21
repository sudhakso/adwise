import nltk.classify
import re, pickle, csv, os
from classifier_helper import ClassifierHelper
import threading
from datetime import datetime


class ClassifierController:
    def __init__(self, training, pickledump, datadir):
        self.training = training
        self.pickledump = pickledump
        self.datadir = datadir
        self.nb = None

    def getNBClassifier(self):
        if self.nb:
            return self.nb
        else:
            self.nb = NaiveBayesClassifier(self.training,
                                           self.pickledump,
                                           self.datadir)
            return self.nb


class NaiveBayesClassifier:
    """ Naive Bayes Classifier """
    def __init__(self, trainingDataFile,
                 classifierDumpFile,
                 datadir):
        # Instantiate classifier helper
        self.helper = ClassifierHelper(
                                '%s/%s' % (datadir,
                                               'feature_list.txt'),
                                '%s/%s' % (datadir,
                                               'stop_words.txt'))
        self.trainingDataFile = trainingDataFile
        self.classifierPickled = classifierDumpFile
        self.last_trained = None
        self.classifier = self._getClassifier()

    def _getClassifier(self, reload_existing=False):
        import os.path
        # Record time.
        self.time = datetime.now()
        if reload_existing:
            if os.path.exists(self.classifierPickled):
                f1 = open(self.classifierPickled)
                if(f1):
                    self.classifier = pickle.load(f1)
                    f1.close()
                    return
        return self._getNBTrainedClassifer(self.trainingDataFile,
                                           self.classifierPickled)

    def _getUniqData(self, data):
        uniq_data = {}
        for i in data:
            d = data[i]
            u = []
            for element in d:
                if element not in u:
                    u.append(element)
            # end inner loop
            uniq_data[i] = u
        # end outer loop
        return uniq_data

    # start getProcessedTweets
    def _getProcessedTweets(self, data):
        tweets = {}
        for i in data:
            d = data[i]
            tw = []
            for t in d:
                tw.append(self.helper.process_tweet(t))
            tweets[i] = tw
        # end loop
        return tweets

    def _getNBTrainedClassifer(self, trainingDataFile, classifierDumpFile):
        # read all tweets and labels
        tweets = self._getFilteredTrainingData(trainingDataFile)
        training_set = nltk.classify.apply_features(
                                        self.helper.extract_features,
                                        tweets)
        # Write back classifier and word features to a file
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        outfile = open(classifierDumpFile, 'wb')
        pickle.dump(classifier, outfile)
        outfile.close()
        return classifier

    def _getFilteredTrainingData(self, _file):
        inpTweets = csv.reader(open(_file, 'rb'),
                               delimiter=',',
                               quotechar='|')
        count = 0
        featureList = []
        tweets = []
        for row in inpTweets:
            if len(row) < 2:
                continue
            category = row[0]
            tweet = row[1]
            processedTweet = self.helper.process_tweet(tweet)
            featureVector = self.helper.getFeatureVector(processedTweet)
            featureList.extend(featureVector)
            tweets.append((featureVector, category))
        return tweets

    # classify words
    def classify(self, message):
        processedTestTweet = self.helper.process_tweet(message)
        classification = self.classifier.classify(
                                    self.helper.extract_features(
                                            self.helper.getFeatureVector(
                                                    processedTestTweet)))
        return classification
