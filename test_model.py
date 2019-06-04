import pickle
import numpy as np
from logistic_reg_tf_idf import read_files, read_unlabeled_input,pred_text_input, tsv_new_read_files

class Data:pass

def load_pickle_sentiment(pickle_file):
    sentiment_list = []
    with open(pickle_file,'rb') as f:
        while True:
            try:
                sentiment_list.append(pickle.load(f))
            except EOFError:
                break
    sentiment = sentiment_list[0]
    top_k_words = sentiment_list[1]
    bottom_k_words = sentiment_list[2]
    return sentiment, top_k_words, bottom_k_words

def test_model(input_str, file_choice):
    file_sent_model = 'sentiment_model.sav'
    file_toxic_model = 'toxicity_model.sav'

    tarfnameSent = "data/sentiment.tar.gz"
    tarfnameToxic = "data/toxicData.tar.gz"

    if (file_choice == "toxic"):
        loaded_model = pickle.load(open(file_toxic_model, 'rb'))
        count_data, top_k_words, bottom_k_words = load_pickle_sentiment('sentiment_train')
        # count_data = tsv_new_read_files(tfidf=True,max_df=0.5)
        # count_data = load_pickle_sentiment('sentiment_train')

    elif(file_choice == "sentiment"):
        loaded_model = pickle.load(open(file_sent_model, 'rb'))
        count_data, top_k_words, bottom_k_words = load_pickle_sentiment('original_train')
        # count_data = read_files(tarfnameSent,tfidf= True, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1))
        # count_data = load_pickle_sentiment('original_train')
    else:
        sys.exit()

    print("\nReading input data")
    unlabeled = read_unlabeled_input(input_str, count_data)     # "you are very good nice"
    # unlabeled = read_unlabeled(tarfname, sentiment)
    print("Making prediction: \n")
    print("input string: "+ input_str + "\n")
    (label, confidence) = pred_text_input(unlabeled, loaded_model, "data/sentiment-pred.csv", count_data)

    k = 300
    top_k_words  = top_k_words[:k]
    bottom_k_words = bottom_k_words[:k]
    ## TOP K WORDS
    # k = 300
    # coefficients=loaded_model.coef_[0]
    # # get top_k toxic coefficients -> positive coefficients tends to make prediction toxic
    # top_k = np.argsort(coefficients)[-k:]
    # top_k_words = []
    # print("START")
    # for i in top_k:
    #     top_k_words.append(count_data.count_vect.get_feature_names()[i])
    #
    # bottom_k =np.argsort(coefficients)[:k]
    # bottom_k_words = []
    # for i in bottom_k:
    #     # print(count_data.count_vect.get_feature_names()[i])
    #     bottom_k_words.append(count_data.count_vect.get_feature_names()[i])
    # print("END")
    return (label, confidence,top_k_words,bottom_k_words)


if __name__ == "__main__":
    test_model("yes yes fuck worst","toxic")
