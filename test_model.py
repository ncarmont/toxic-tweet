import pickle
from logistic_reg_tf_idf import read_files, read_unlabeled_input,pred_text_input

def test_model(input_str, file_choice):
    file_sent_model = 'sentiment_model.sav'
    file_toxic_model = 'toxicity_model.sav'

    tarfnameSent = "data/sentiment.tar.gz"
    tarfnameToxic = "data/toxicData.tar.gz"

    if (file_choice == "toxic"):
        loaded_model = pickle.load(open(file_toxic_model, 'rb'))
        count_data = read_files(tarfnameToxic,tfidf= True, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1))

    elif(file_choice == "sentiment"):
        loaded_model = pickle.load(open(file_sent_model, 'rb'))
        count_data = read_files(tarfnameSent,tfidf= True, incl_stop_words=False, lowercase=True, max_df=1.0, min_df=1,max_features=None,ngram_range=(1,1))
    else:
        sys.exit()

    print("\nReading input data")
    unlabeled = read_unlabeled_input(input_str, count_data)     # "you are very good nice"
    # unlabeled = read_unlabeled(tarfname, sentiment)
    print("Making prediction: \n")
    print("input string: "+ input_str + "\n")
    (label, confidence) = pred_text_input(unlabeled, loaded_model, "data/sentiment-pred.csv", count_data)

    return (label, confidence)


if __name__ == "__main__":
    test_model("yes yes good good","sentiment")
