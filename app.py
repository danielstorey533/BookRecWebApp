#Enter 'python app.py' to launch webserver in terminal.

#git add *
#git commit
#git push origin master

#Commands used for launching db:
#from app import db (after writing py) - imports our db to shell
#db.create_all()
#exit()


#Imports flask from Flask class -- Flask is a web framework for Python.
#Flask uses Jinja for templates; which is a web template engine.
from flask import Flask, render_template, url_for, request, redirect, g
from datetime import datetime
import recommend
import sqlite3


#Python package which will be used to keep track of session ID's per user.
import flask_login 

from connection import connection

conn, c = connection()


#Cursor fetches return results as tuples so need a function to convert to string;
#used for login and database interactivity.
def convertTuple(tup): 
        str =  ''.join(tup) 
        return str 

#Sets up the app and database. Enter 'python app.py' to launch in terminal.
app = Flask(__name__)
DATABASE = 'test.db'

#Secret key used for cookie/session info.
#FIXME: Change this, placeholder key.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#flask-login class; 
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = '{}' ".format(username))

    user = User()
    user.id = username
    return user


#FIXME: Can probably remove this comment; request_loader seems to be identical to user_loader 
#but for API keys / header values (which I am not using)
#will leave in for now.

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')

#     user = User()
#     user.id = username

#     user.is_authenticated = request.form['password'] == users[username]['password']

#     return user











# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Instantiate SVD Recommender..
s = recommend.SVDRecommender(get_db)

# Instantiate a random recommender.
#r = recommend.RandomRecommender(get_db)

# Instantiate KNN Recommender..
k = recommend.KNNRecommender(get_db)

#Sets up index route which will display index() function when route is visited.
#index() function calls render_template method(which knows to check templates folder) to return our index.html.
#methods enable us to POST and GET from the route (database).
@app.route('/', methods=['POST', 'GET'])
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    #FIXME: Using fetchmany currently to not load all 10k books onto webpage; need to fix how books load; possibly add pages.
    allBooks = c.fetchmany(100)
    userSession = flask_login.current_user.id
    return render_template('index.html', allBooks = allBooks, userSession = userSession)


@app.route('/results', methods=['POST', 'GET'])
def results():
    bookResults = s.get()
    return render_template('results.html', bookResults = bookResults)

@app.route('/knnresults', methods=['POST', 'GET'])
def knnresults():
    bookResults = k.get()
    return render_template('results.html', bookResults = bookResults)

#FIXME: Login will crash if the user is not logged in; look up how to restrict page if user session
#not initalised.

#FIXME: /login should probably return a template with this HTML and code; would make the code a lot cleaner.
#https://docs.python.org/3.8/library/sqlite3.html for inputting variables into SQL query.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                   <input type='password' name='password' id='password' placeholder='password'/>
                  <input type='submit' name='submit'/>
             </form>
             '''

    username = request.form['username']
    passwordVerif = c.execute("SELECT password FROM users WHERE username = '{}'".format(username))
    passwordVerif = c.fetchone()
    passwordVerif = convertTuple(passwordVerif) 

    if request.form['password']== passwordVerif:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


#Post route which will be called on rating form submission (user five star input).
@app.route('/rate/<int:book_id>', methods=['POST'])
@flask_login.login_required
def rate(book_id):
    conn = get_db()
    c = conn.cursor()
    rating = request.form.get('rating')
    user_id = 1
    #FIXME: Hardcoding this as 1 for now; will need to call the allBook id from index.html template somehow.


    q = c.execute('SELECT * FROM ratings WHERE book_id == ' + str(book_id) + ' and user_id == ' + str(user_id))
    check = q.fetchall()

    if(len(check) < 1):
        c.execute('INSERT INTO ratings (user_id, book_id, rating) VALUES (?, ?, ?)',
        (user_id, book_id, rating))
        conn.commit()
        
        print('successfully added')
        return 'Successfully added'

    else: c.execute('UPDATE ratings set rating == ' + str(rating) + ' WHERE book_id == ' + str(book_id) 
    + ' AND user_id == ' + str(user_id))

    print('successfully updated')
    return ' Successfully added'






#Enables debug mode which displays errors on webpage.
if __name__ == "__main__":
    app.run(debug=True)
