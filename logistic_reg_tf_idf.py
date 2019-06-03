# CLASSIFIER
import sys
import json
import csv
import pickle

def train_classifier(X, y, regType='lbfgs'): #regType='lbfgs'):
    """Train a classifier using the given training data.

    Trains logistic regression on the input data with default parameters.
    """
    from sklearn.linear_model import LogisticRegression
    cls = LogisticRegression(random_state=0, solver=regType, max_iter=10000) # max_iter=10000)
    cls.fit(X, y)
    return cls

def evaluate(X, yt, cls, name='data',doesPrint="yes", doesReturn="no"):
    """Evaluated a classifier on the given labeled data using accuracy."""
    from sklearn import metrics
    yp = cls.predict(X)
    acc = metrics.accuracy_score(yt, yp)
    if (doesPrint=="yes"):
        print("  Accuracy on %s  is: %s" % (name, acc))
    if(doesReturn =="yes"):
        return acc

# SENTIMENT ANALYIS

def read_files(tarfname,tfidf= False, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1)):
    """Read the training and development data from the sentiment tar file.
    The returned object contains various fields that store sentiment data, such as:

    train_data,dev_data: array of documents (array of words)
    train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
    train_labels,dev_labels: the true string label for each document (same length as data)

    The data is also preprocessed for use with scikit-learn, as:

    count_vec: CountVectorizer used to process the data (for reapplication on new data)
    trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
    le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
    target_labels: List of labels (same order as used in le)
    trainy,devy: array of int labels, one for each document
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    trainname = "train.tsv"
    devname = "dev.tsv"
    for member in tar.getmembers():
        if 'train.tsv' in member.name:
            trainname = member.name
        elif 'dev.tsv' in member.name:
            devname = member.name


    class Data: pass
    sentiment = Data()
    print("-- train data")
    sentiment.train_data, sentiment.train_labels = read_tsv(tar,trainname)
    print(len(sentiment.train_data))

    print("-- dev data")
    sentiment.dev_data, sentiment.dev_labels = read_tsv(tar, devname)
    print(len(sentiment.dev_data))
    print("-- transforming data and labels")
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer #CountVectorizer()
    if(tfidf==True):
        if(incl_stop_words):
            sentiment.count_vect = TfidfVectorizer(stop_words='english',lowercase=lowercase, max_df=max_df, min_df=min_df,max_features=max_features,ngram_range=ngram_range)
        else:
            sentiment.count_vect = TfidfVectorizer(stop_words=None,lowercase=lowercase, max_df=max_df, min_df=min_df,max_features=max_features,ngram_range=ngram_range)
    else:
        if(incl_stop_words):
            sentiment.count_vect = CountVectorizer(stop_words='english',lowercase=lowercase, max_df=max_df, min_df=min_df,max_features=max_features,ngram_range=ngram_range)
        else:
            sentiment.count_vect = CountVectorizer(stop_words=None,lowercase=lowercase, max_df=max_df, min_df=min_df,max_features=max_features,ngram_range=ngram_range)

    sentiment.trainX = sentiment.count_vect.fit_transform(sentiment.train_data)
    sentiment.devX = sentiment.count_vect.transform(sentiment.dev_data)
    from sklearn import preprocessing
    sentiment.le = preprocessing.LabelEncoder()
    sentiment.le.fit(sentiment.train_labels)
    sentiment.target_labels = sentiment.le.classes_
    sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
    sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
    tar.close()
    return sentiment


def read_unlabeled_input(input_str, sentiment):
    class Data: pass
    unlabeled = Data()
    unlabeled.data = []
    text = input_str.strip()
    unlabeled.data.append(text)

    unlabeled.X = sentiment.count_vect.transform(unlabeled.data)
    print(unlabeled.X.shape)

    return unlabeled



def read_unlabeled(tarfname, sentiment):
    """Reads the unlabeled data.

    The returned object contains three fields that represent the unlabeled data.

    data: documents, represented as sequence of words
    fnames: list of filenames, one for each document
    X: bag of word vector for each document, using the sentiment.vectorizer
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    class Data: pass
    unlabeled = Data()
    unlabeled.data = []

    unlabeledname = "unlabeled.tsv"
    for member in tar.getmembers():
        if 'unlabeled.tsv' in member.name:
            unlabeledname = member.name

    print(unlabeledname)
    tf = tar.extractfile(unlabeledname)
    for line in tf:
        line = line.decode("utf-8")
        text = line.strip()
        unlabeled.data.append(text)


    unlabeled.X = sentiment.count_vect.transform(unlabeled.data)
    print(unlabeled.X.shape)
    tar.close()
    return unlabeled

def read_tsv(tar, fname):
    member = tar.getmember(fname)
    print(member.name)
    tf = tar.extractfile(member)
    data = []
    labels = []
    for line in tf:
        line = line.decode("utf-8")
        if len(line.strip().split("\t")) ==2:
            (label,text) = line.strip().split("\t")
            labels.append(label)
            data.append(text)
    return data, labels




def pred_text_input(unlabeled, cls, outfname, sentiment):
    """Writes the predictions in Kaggle format.

    Given the unlabeled object, classifier, outputfilename, and the sentiment object,
    this function write sthe predictions of the classifier on the unlabeled data and
    writes it to the outputfilename. The sentiment object is required to ensure
    consistent label names.
    """
    yp = cls.predict(unlabeled.X)
    labels = sentiment.le.inverse_transform(yp)
    print("THIS IS SENTIMENT")
    print(type(sentiment))
    conf = cls.predict_proba(unlabeled.X)
    print(unlabeled.X)
    label = labels[0]
    if (str(labels[0]) == "NEGATIVE"):
        confidence = conf[0][0]
        print("pred:" + str(labels[0])+" confidence: "+str(confidence)+ "\n")
    else:
        confidence = conf[0][1]
        print("pred:" + str(labels[0])+" confidence: "+str(confidence)+ "\n")

    return (label,confidence)


def write_pred_kaggle_file(unlabeled, cls, outfname, sentiment):
    """Writes the predictions in Kaggle format.

    Given the unlabeled object, classifier, outputfilename, and the sentiment object,
    this function write sthe predictions of the classifier on the unlabeled data and
    writes it to the outputfilename. The sentiment object is required to ensure
    consistent label names.
    """
    yp = cls.predict(unlabeled.X)
    labels = sentiment.le.inverse_transform(yp)
    f = open(outfname, 'w')
    f.write("ID,LABEL\n")
    for i in range(len(unlabeled.data)):
        f.write(str(i+1))
        f.write(",")
        f.write(labels[i])
        f.write("\n")
    f.close()


def write_gold_kaggle_file(tsvfile, outfname):
    """Writes the output Kaggle file of the truth.

    You will not be able to run this code, since the tsvfile is not
    accessible to you (it is the test labels).
    """
    f = open(outfname, 'w')
    f.write("ID,LABEL\n")
    i = 0
    with open(tsvfile, 'r') as tf:
        for line in tf:
            (label,review) = line.strip().split("\t")
            i += 1
            f.write(str(i))
            f.write(",")
            f.write(label)
            f.write("\n")
    f.close()

def write_basic_kaggle_file(tsvfile, outfname):
    """Writes the output Kaggle file of the naive baseline.

    This baseline predicts POSITIVE for all the instances.
    """
    f = open(outfname, 'w')
    f.write("ID,LABEL\n")
    i = 0
    with open(tsvfile, 'r') as tf:
        for line in tf:
            (label,review) = line.strip().split("\t")
            i += 1
            f.write(str(i))
            f.write(",")
            f.write("POSITIVE")
            f.write("\n")
    f.close()


# TRAINING
if __name__ == "__main__":
    tarfnameSent = "data/sentiment.tar.gz"
    tarfnameToxic = "data/toxicData.tar.gz"

    print("\nTraining classifiers")
    sentiment = read_files(tarfnameSent,tfidf= True, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1))
    toxicity = read_files(tarfnameToxic,tfidf= True, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1))

    clsSent = train_classifier(sentiment.trainX, sentiment.trainy)
    clsToxic = train_classifier(toxicity.trainX, toxicity.trainy)

    file_sent_model = 'sentiment_model.sav'
    file_toxic_model = 'toxicity_model.sav'

    pickle.dump(clsSent, open(file_sent_model, 'wb'))
    pickle.dump(clsToxic, open(file_toxic_model, 'wb'))

    print("\nEvaluating Sent")
    evaluate(sentiment.trainX, sentiment.trainy, clsSent, 'train')
    evaluate(sentiment.devX, sentiment.devy, clsSent, 'dev')

    print("\nEvaluating Toxic")
    evaluate(toxicity.trainX, toxicity.trainy, clsToxic, 'train')
    evaluate(toxicity.devX, toxicity.devy, clsToxic, 'dev')
