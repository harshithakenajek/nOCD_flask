import os

from flask import Flask, render_template, request, url_for, redirect,make_response, session
app = Flask(__name__)

# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import logging 
from logging.handlers import RotatingFileHandler

engine =create_engine("mysql://root:root@localhost:5000/python_flask_app")
connection = engine.connect()


@app.route('/login', methods = ['POST','GET'])
def login_user():
    error = None
    if request.method == 'POST':
        if login_valid_user(request.form['username'],request.form['password']):
            #  # if used cookies
            # response = make_response(redirect(url_for('welcome')))
            # response.set_cookie('username',request.form.get('username'))
            # return response
            # if used sessions
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error ="Invalid username and password"
            app.logger.warning("Incorrect username and password for the user %s", request.form['username'])
            return render_template('login.html',error=error)
    else:
        return render_template('login.html')
        
def login_valid_user( username, password ):
    user = connection.execute("SELECT * FROM user WHERE user_name = '%s' AND password = '%s' " %(username,password))
    # userdata = db.fetchall()
    print('The user data')
    for userdata in user:
        print(userdata)
        if userdata:
            return True
        else: 
            return False

@app.route('/')
def welcome():
    if 'username' in session: 
        return render_template('welcome.html',username=session['username'])
    else:
        return render_template('login.html')

@app.route('/logout')
def logout_user():
    # # if used cookies
    # response = make_response(redirect(url_for('login_user')))    
    # response.set_cookie('username','',expires=0)
    # return response

    # if used sessions
    session.pop('username',None)
    return redirect(url_for('login_user'))

if __name__ == '__main__':
    app.debug = True
    app.secret_key ='x\xc1\x06\xfb3\xb9\x9b4\xcf\x9e\xbc[\xed\x9e\x05P\xe5\xeb5\xc2zE\xe1j'

    # logging
    handler = RotatingFileHandler('error.log',maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000))))
