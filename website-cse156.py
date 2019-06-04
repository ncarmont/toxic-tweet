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


# BOOSTRAP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


class userInputForm(FlaskForm):

    input_str = StringField('', validators=[])
    sent_analysis = SubmitField('😊 Sentiment Analysis')  # ☻
    toxic_analysis = SubmitField('⚠️ Toxic Comment Analysis')
    submit = SubmitField('Tweet')


# ROUTES
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    global file_choice
    global init_file_choice
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

    elif form.toxic_analysis.data:
        file_choice ="toxic"
        message = "Detect: Toxicity"

    elif form.validate_on_submit() and form.input_str.data:
        input_text = form.input_str.data
        (l,c,bottom_k_words,top_k_words) = test_model(input_text,file_choice)

        # TOP K top_k_words

        toxic_words = ''
        for tw in top_k_words:
            toxic_words = toxic_words + tw + ' '

        cloud_words = ''

        words_in_bad_cloud = False
        for w in input_text.split(' '):
            if w in toxic_words:
                cloud_words = cloud_words + w + ' '
                words_in_bad_cloud = True



        stopwords = set(STOPWORDS)
        if words_in_bad_cloud:
            wordcloud = WordCloud(width = 512, height = 512,
                            background_color ='black',
                            stopwords = stopwords,
                            min_font_size = 10).generate(cloud_words)
            wordCloud_bad = 'static/images/wordCloud_top.png'
            wordcloud.to_file(wordCloud_bad)
    wordCloud_bad_file = "images/wordCloud_top.png"


        # message = "Label: "+ str(l) +"-------- Confidence: "+ str(c)


    return render_template('index.html', wordCloud_bad=wordCloud_bad_file, message=message, form=form, label= str(l), confidence = int(c*100), str_conf = str(c))

if __name__ == '__main__':
    app.run(debug=True)
