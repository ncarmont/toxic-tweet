# using python 3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from test_model import test_model
import os

# DEFAULT
file_choice = "sentiment"
init_file_choice = True


# BOOSTRAP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


class userInputForm(FlaskForm):
    sent_analysis = SubmitField('Sentiment Analysis')
    toxic_analysis = SubmitField('Toxic Comment Analysis')
    input_str = StringField('Type in some text for us: ', validators=[])
    submit = SubmitField('Run prediction')


# ROUTES
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    global file_choice
    global init_file_choice

    message = ""
    form = userInputForm()

    if init_file_choice:
        file_choice ="sentiment"
        init_file_choice = False



    if form.sent_analysis.data:
        file_choice ="sentiment"

    elif form.toxic_analysis.data:
        file_choice ="toxic"
        message = "toxic"

    elif form.validate_on_submit() and form.input_str.data:
        input_text = form.input_str.data
        (l,c) = test_model(input_text,file_choice)

        message = "Label: "+ str(l) +"-------- Confidence: "+ str(c)



    return render_template('index.html', form=form, message=message)


if __name__ == '__main__':
    app.run(debug=True)
