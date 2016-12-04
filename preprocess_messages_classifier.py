import csv
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from nltk import NaiveBayesClassifier, classify
import pickle

def preprocess(sentence):
    return [wordnet_lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)]

def get_features(text, setting):
    if setting == 'bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}

def train(features, samples_proportion):
    train_size = int(len(features) * samples_proportion)
    train_set, test_set = features[:train_size], features[train_size:]
    print('Training set size = ' + str(len(train_set)) + ' messages')
    print('Test set size = ' + str(len(test_set)) + ' messages')
    classifier = NaiveBayesClassifier.train(train_set)
    return train_set, test_set, classifier

# evaluate classifier
def evaluate(train_set, test_set, classifier):
    print('Accuracy on the training set = ' + str(classify.accuracy(classifier, train_set)))
    print('Accuracy of the test set = ' + str(classify.accuracy(classifier, test_set)))

training_data = []
training_labels = []
with open('export.csv', newline='') as csvfile:
    csv_object = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in csv_object:
        training_data.append(row[0])
        training_labels.append(row[1])

stoplist = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()

all_features = [(get_features(data, 'bow'), label) for (data, label) in zip(training_data, training_labels)]

train_set, test_set, classifier = train(all_features, 0.8)
evaluate(train_set, test_set, classifier)
classifier.show_most_informative_features(20)

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier, protocol=2)
save_classifier.close()

fs = get_features("python is a great programming language", 'bow')
label = classifier.prob_classify(fs)
print(label.prob('on'), label.prob('off'))

fs2 = get_features("women", 'bow')
label2 = classifier.prob_classify(fs2)
print(label2.prob('on'), label2.prob('off'))
