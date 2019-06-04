#! /usr/bin/env python
# using python 3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from test_model import test_model
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import random as random
from PIL import Image
import urllib
import requests

# DEFAULT
file_choice = "sentiment"
init_file_choice = True
cloud_1= "Top Negative Words"
cloud_2 = "Top Positive Words"
class Data:pass

# BOOSTRAP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


class userInputForm(FlaskForm):

    input_str = StringField('', validators=[])
    # new = SubmitField('😊 new')  # ☻
    sent_analysis = SubmitField('😊 Sentiment Analysis')  # ☻
    toxic_analysis = SubmitField('⚠️ Toxic Comment Analysis')
    submit = SubmitField('Tweet')


# ROUTES
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    global file_choice
    global init_file_choice
    global cloud_1
    global cloud_2

    message = "Detect: " + file_choice

    form = userInputForm()

    l = ""
    c = 0

    if init_file_choice:
        file_choice ="sentiment"
        init_file_choice = False

    if form.sent_analysis.data:
        file_choice ="sentiment"
        message = "Detect: Sentiment"
        cloud_1= "Top Negative Words"
        cloud_2 = "Top Positive Words"

    elif form.toxic_analysis.data:
        file_choice ="toxic"
        message = "Detect: Toxicity"
        cloud_1 = "Top Non-Toxic Words"
        cloud_2 = "Top Toxic Words"

    elif form.validate_on_submit() and form.input_str.data:
        input_text = form.input_str.data
        (l,c,bottom_k_words,top_k_words) = test_model(input_text.lower(),file_choice)

        # TOP K top_k_words

        toxic_words = ''
        for tw in top_k_words:
            # print(tw)
            toxic_words = toxic_words + tw + ' '

        print("\n\n\n\n")
        non_toxic_words = ''
        for tw in bottom_k_words:
            # print(tw)
            non_toxic_words = non_toxic_words + tw + ' '

        non_toxic_cloud_words = ''
        words_in_good_cloud = False
        for w in input_text.split(' '):
            if w in non_toxic_words and len(w) > 2:
                non_toxic_cloud_words = non_toxic_cloud_words + w + ' '
                words_in_good_cloud = True


        toxic_cloud_words = ''
        words_in_bad_cloud = False
        for w in input_text.split(' '):
            if w in toxic_words and len(w) > 2:
                toxic_cloud_words = toxic_cloud_words + w + ' '
                words_in_bad_cloud = True

        stopwords = set(STOPWORDS)

        if words_in_bad_cloud:
            wordcloud = WordCloud(width = 512, height = 512,
                            background_color ='black',
                            stopwords = stopwords,
                            min_font_size = 10).generate(toxic_cloud_words)
            wordCloud_good = 'static/images/wordCloud_toxic.png'
            wordcloud.to_file(wordCloud_good)
        else:
            wordcloud = WordCloud(width = 512, height = 512,
                            background_color ='black',
                            stopwords = stopwords,
                            min_font_size = 10).generate('None-found')
            wordCloud_good = 'static/images/wordCloud_toxic.png'
            wordcloud.to_file(wordCloud_good)


        if words_in_good_cloud:
            wordcloud = WordCloud(width = 512, height = 512,
                            background_color ='black',
                            stopwords = stopwords,
                            min_font_size = 10).generate(non_toxic_cloud_words)
            wordCloud_bad = 'static/images/wordCloud_non_toxic.png'
            wordcloud.to_file(wordCloud_bad)
        else:
            wordcloud = WordCloud(width = 512, height = 512,
                            background_color ='black',
                            stopwords = stopwords,
                            min_font_size = 10).generate('None-found')
            wordCloud_bad = 'static/images/wordCloud_non_toxic.png'
            wordcloud.to_file(wordCloud_bad)


    wordCloud_bad_file = "images/wordCloud_toxic.png"
    wordCloud_good_file = "images/wordCloud_non_toxic.png"


        # message = "Label: "+ str(l) +"-------- Confidence: "+ str(c)


    return render_template('index.html', detect = file_choice, cloud_1 = cloud_1, cloud_2 =cloud_2, word_cloud_good=wordCloud_good_file, wordCloud_bad=wordCloud_bad_file, message=message, form=form, label= str(l), confidence = int(c*100), str_conf = str(c))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



if __name__ == '__main__':
    app.run(debug=True)
