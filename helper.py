import os
import sys
import re
import pickle
import string
import json

#Converts data file to [rating, [[word, count],..]]
def parseFile(newFile):
    res = []
    #Opens File
    with open(newFile, 'r') as fp:
        for line in fp:
            #Splits line into a list of [word, count]
            features = [x.split(":") for x in line.split()]
            rating = features[-1][1]

            #Add to result
            res.append([rating, features[:-1]])
    return res

#Normalizes a list
def normalize(lst):
    res = []
    for x in lst:
        res.append(x/sum(lst))
    return res 

#def save_file(obj, name):
 #   with open(name + '.pkl', 'wb') as f:
  #      pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def save_file(obj, name):
   with open(name + '.json', 'wb') as f:
    json.dump(obj, f)

def read_file(name):
    with open(name + '.json', 'r') as f:
        return json.load(f)

#def read_file(name):
 #   with open(name + '.pkl', 'r') as f:
  #      return pickle.load(f)

def remove_punct(s):
    return s.translate(string.maketrans("",""), string.punctuation)

def print_res(res):
    neg = res[0] + res[1]
    pos = res[3] + res[4]
    if neg > pos:
        print "Predicted Sentiment is Negative with %.2d percent confidence." % (neg*100)
    elif pos > neg:
        print "Predicted Sentiment is Positive with %.2d percent confidence." % (pos*100)
    else:
        print "Ambiguous review."
    print "Predicted Rating is %d stars." % (res.index(max(res)) + 1)
    print res
