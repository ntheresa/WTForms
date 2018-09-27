from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

class ArtistForm(FlaskForm):
    artist = StringField('Artist Name ', validators = [Required()])
    number_of_results = IntegerField('Number of results you want returned ', validators=[Required()])
    email = StringField('Enter your email ', validators = [Required(), Email()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form

@app.route('/itunes-form', methods = ['GET', 'POST'])
def itunes_form():
    simpleForm = ArtistForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = ArtistForm(request.form)
    params = {}
    if request.method == 'POST' and form.validate_on_submit():
        params['term'] = form.artist.data
        params['limit'] = form.number_of_results.data
        response = requests.get('https://itunes.apple.com/search?', params=params)
        response_text = json.loads(response.text)
        result_list = response_text['results']
        print(result_list)
        return render_template('itunes-results.html', result_html=result_list)


    # HINT : create itunes-results.html to represent the results and return it
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
