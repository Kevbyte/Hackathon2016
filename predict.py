from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
import json
import numpy as np
import operator

def read_data(fname):
  f = open(fname, 'rb')
  texts = []
  ys = []
  for line in f:
    rec = json.loads(line.strip())
    texts.append(rec["text"])
    yvector = [0,0,0,0,0]
    rating = rec["stars"] 
    yvector[rating - 1] = 1;
    ys.append(yvector)
  f.close()
  return texts, np.matrix(ys)

def vectorize(texts, vocab=[]):
  vectorizer = CountVectorizer(min_df=0, stop_words="english") 
  if len(vocab) > 0:
    vectorizer = CountVectorizer(min_df=0, stop_words="english", 
      vocabulary=vocab)
  X = vectorizer.fit_transform(texts)
  return vectorizer.vocabulary_, X
word_features = [
'told'
'worst'
'manager'
'said'
'horrible'
'rude'
'asked'
'minutes'
'terrible'
'called'

'bland'
'ok'
'mediocre'
'better'
'minutes'
'just'
'asked'
'didn'
'wasn'
'meh'

'ok'
'good'
'decent'
'pretty'
'okay'
'average'
'wasn'
'stars'
'bit'
'overall'

'good'
'told'
'nice'
'great'
'asked'
'tasty'
'little'
'customer'
'manager'
'worst'

'amazing'
'good'
'best'
'pretty'
'didn'
'love'
'ok'
'like'
'bad'
'wasn'
]



word_features = get_word_features(get_words_in_tweets(tweets))
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def cross_validate(ufc_val, X, y, nfeats):
  nrows = X.shape[0]
  kfold = KFold(nrows, 10)
  scores = []
  for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = X[train], X[test], y[train], y[test]
    clf = MultinomialNB()
    clf.fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    accuracy = accuracy_score(ytest, ypred)
    precision = precision_score(ytest, ypred)
    recall = recall_score(ytest, ypred)
    scores.append((accuracy, precision, recall))
  print ",".join([ufc_val, str(nfeats), 
    str(np.mean([x[0] for x in scores])),
    str(np.mean([x[1] for x in scores])),
    str(np.mean([x[2] for x in scores]))])


def main():
  #ufc = {0:"useful", 1:"funny", 2:"cool"}
   ufc = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4"}
#   texts, ys = read_data("unit_testing.json")
   texts, ys = read_data("yelp_academic_dataset_review.json")
   print ",".join(["attrtype", "nfeats", "accuracy", "precision", "recall"])
   for ufc_idx, ufc_val in ufc.items():
	#print ys
   	y = ys[:, ufc_idx].A1
   	V, X = vectorize(texts)
    	cross_validate(ufc_val, X, y, -1)
    	sorted_feats = sorted_features(ufc_val, V, X, y, 10)
    	for nfeats in [1000, 3000, 10000, 30000, 100000]:
      		V, X = vectorize(texts, sorted_feats[0:nfeats])
      		cross_validate(ufc_val, X, y, nfeats)

if __name__ == "__main__":
  main()
