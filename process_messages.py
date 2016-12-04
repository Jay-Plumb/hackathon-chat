import pickle
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
import json
def process(json_data):
    # Classifies messages in JSON file as being either on-topic, off-topic, or undecided
    # Inputs: JSON file
    # Output: JSON file with markdowns

 
    # import requests

    def preprocess(sentence):
        return [wordnet_lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)]

    def get_features(text, setting):
        if setting == 'bow':
            return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
        else:
            return {word: True for word in preprocess(text) if not word in stoplist}

    # load classifier
    classifier_f = open("naivebayes.pickle", "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()

    # load stoplist and lemmatizer
    stoplist = stopwords.words('english')
    wordnet_lemmatizer = WordNetLemmatizer()
    data = json.loads(open(json_data).read())
    # classify text
    messages = []
    labels = []
    for item in data["items"]:
        message = (item["text"])
        messages.append(message)
        fs = get_features(message, 'bow')
        prob_dist = classifier.prob_classify(fs)
        prob_on = prob_dist.prob('on')
        prob_off = prob_dist.prob('off')
        if prob_on >= 0.5 and prob_off <= 0.5:
            label = '1'
            item["markdown"] = "<h1>" + message + "</h1>"
        elif prob_on <= 0.5 and prob_off >= 0.5:
            label = '3'
            item["markdown"] = "### " + message + "\n"
        else:
            label = '2'
            item["markdown"] = "## " + message + "\n"
        item["label"] = label

    return data

