import os
import time
from datetime import timedelta

from flask import Flask, render_template, flash, request, redirect, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from tweetfollowers import Twitter_Followers
from tweetfollowers import Twitter_User_Keyword
from login_sql import LoginPage

# App config. 
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(12)

class TweeterFollowers(Form):
    name_a = TextField('Screen Name of Follower A:', validators=[validators.required()])
    name_b = TextField('Screen Name of Follower B:', validators=[validators.required()])
    
class TweetKeyword(Form):
    name = TextField('Screen Name:', validators=[validators.required()])
    word = TextField('Keyword:', validators=[validators.required()])

class Login(Form):
    username = TextField('Username:', validators=[validators.required()])
    password = TextField('Password', validators=[validators.required()])

class Register(Form):
    f_name = TextField('First Name:', validators=[validators.required()])
    l_name = TextField('Last Name:', validators=[validators.required()])
    email = TextField('Last Name:', validators=[validators.required()])
    password = TextField('Last Name:', validators=[validators.required()])


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/login', methods=['POST'])
def do_admin_login():

    form = Login(request.form)
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        #validating Form
        if form.validate():
            # calling class
            valid = LoginPage()
            data = valid.sign_in(username,password)
            if data == True:
                session['logged_in'] = True
            else:
                flash('Username or password does not match our database')
        else:
            flash('Error: All the form fields are required. ')      
    return common_followers()

@app.errorhandler(404)
def page_not_found(e):
    form = Login(request.form)
    return render_template('login.html', form=form), 404

@app.errorhandler(405)
def method_not_allowed(e):
    form = Login(request.form)
    return render_template('login.html', form=form), 405

@app.route("/", methods=['GET', 'POST']) 
def common_followers():
    if not session.get('logged_in'):
        form = Login(request.form)
        return render_template('login.html', form=form)
    else:
        form = TweeterFollowers(request.form)     
        return render_template('index.html', form=form)

@app.route("/commonfollowers", methods=['POST','GET'])        
def common_followers_output():
    if not session.get('logged_in'):
        form = Login(request.form)
        return render_template('login.html', form=form)
    else:
        form = TweeterFollowers(request.form) 
        if request.method == 'POST':
            name_a=request.form['name_a']
            name_b=request.form['name_b']
            #validating Form
            if form.validate():
                # calling class
                valid = Twitter_Followers()
                #calculating percentage of loan requested
                followers = valid.common_followers(name_a,name_b)
                flash(followers)
            else:
                flash('Error: All the form fields are required. ')   
    return render_template('index.html', form=form)
@app.route("/findtweetkeyword", methods=['GET', 'POST'])
def find_tweet_keyword():
    if not session.get('logged_in'):
        form = Login(request.form)
        return render_template('login.html', form=form)
    else:
        find_tweet_keyword_output()
        form = TweetKeyword(request.form) 
        return render_template('keyword_search.html', form=form)
       
def find_tweet_keyword_output():
    form = TweetKeyword(request.form)
    if request.method == 'POST':
        name = request.form['name']
        word = request.form['word']

        if form.validate():
            # calling class
            valid = Twitter_User_Keyword()
            # get data from csv
            data = valid.tweet_keyword(name,word)
            for i in data:
                flash(i)
        else:
            flash('Error: All the form fields are required. ') 
    return render_template('keyword_search.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():

    form = Register(request.form)

    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if form.validate():
            # calling class
            valid = LoginPage()
            # signup
            data = valid.sign_up(f_name, l_name, username, email, password)
            if data == True:
                flash('Successfully Signed Up')
            else:
                flash(data)
        else:
            flash('Error: All the form fields are required. ')
    return render_template('register.html', form=form)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(debug=True,host='127.0.0.1',port=5000)

