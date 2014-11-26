from helper import *

#Given a word and a model, generates the posterior probability for each rating
def rateWord(word, model):
    #result list is uniformly distributed by default
    res = [0.2, 0.2, 0.2, 0.2, 0.2]
    if word in model:
        c = 0
        
        #Calculates posterior for all possible rating
        for i in ['1.0', '2.0', '3.0', '4.0', '5.0']:
            if model['num_'+ i] > 0:
                p_word_class = model[word][i]/model['num_'+i]
            else:
                p_word_class = 0.
            prior = model['num_' + i] / model['num_words']
            p_word = model[word]['total'] / model['num_words']
            post = p_word_class * prior / p_word
            res[c] = post
            c += 1
    return res

#Returns predicted rating of result list
def predictRating(prob):
    return max(prob)

#Returns positive, negative, or neutral on result list
def predictPositive(prob):
    neg = prob[0] + prob[1]
    neutral = prob[2]
    pos = prob[3] + prob[4]
    
    if pos > neg and pos > neutral:
        return 1
    elif neg > pos and neg > neutral:
        return -1
    else:
        return 0
        
#Returns positive, negative, neutral of rating
def convertRating(r):
    if r == "1.0" or r == "2.0":
        return -1
    elif r == "4.0" or r == "5.0":
        return 1
    else:
        return 0

#Returns true if rating prediction is correct
def is_correct_Rating(prediction):
    rating = prediction[0]
    prob = prediction[1]
    if float(rating) == float(prediction.index(max(prediction))):
        return True
    else:
        return False

#Returns true if pos/neg prediction is correct
def is_correct_Positive(prediction):
    rating = prediction[0]
    prob = prediction[1]
    if convertRating(rating) == predictPositive(prob):
        return True
    else:
        return False


#Classify a review from test dataSet
def classifyData(review, model):
  rating = review[0]
  features = review[1]
  res = [0., 0., 0., 0., 0.] 
  for feature in features:
    word = feature[0]
    postList = rateWord(word, model)
    res = list(map(sum, zip(res, postList)))
  return (rating, normalize(res))  

#Returns number correct for a data file
def classifyFile(testFile, model):
    num_correct = 0
    total_reviews = 0

    fp = parseFile(testFile)
    for review in fp:
        total_reviews += 1
        if is_correct_Positive(classifyData(review,model)):
            num_correct += 1
    return [num_correct, total_reviews]


#Classify review from user input
def classifyInput(review, model):
    res = [0., 0., 0., 0., 0.]

    for word in review:
        #w = remove_punct(word.lower())
        w = word.lower()
        postList = rateWord(w, model)
        res = list(map(sum, zip(res, postList)))

    return normalize(res)
def run_test():
    books_test = classifyFile('./processed_stars/books/test', books_model)
    dvd_test = classifyFile('./processed_stars/dvd/test', dvd_model)
    electronics_test = classifyFile('./processed_stars/electronics/test', electronics_model)
    kitchen_test = classifyFile('./processed_stars/kitchen/test', kitchen_model)

    books_percent = float(books_test[0]) / float(books_test[1]) * 100.0
    dvd_percent = float(dvd_test[0]) / float(dvd_test[1]) * 100.0
    electronics_percent = float(electronics_test[0]) / float(electronics_test[1]) * 100.0
    kitchen_percent = float(kitchen_test[0]) / float(kitchen_test[1]) * 100.0

    print "Correctly classified %d out of %d reviews. (%.2f percent)" % (books_test[0], books_test[1], books_percent)
    print "Correctly classified %d out of %d reviews. (%.2f percent)" % (dvd_test[0], dvd_test[1], dvd_percent)
    print "Correctly classified %d out of %d reviews. (%.2f percent)" % (electronics_test[0], electronics_test[1], electronics_percent)
    print "Correctly classified %d out of %d reviews. (%.2f percent)" % (kitchen_test[0], kitchen_test[1], kitchen_percent)


