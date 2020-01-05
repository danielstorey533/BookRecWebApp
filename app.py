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

from connection import connection

conn, c = connection()



#Sets up the app and database. Enter 'python app.py' to launch in terminal.
app = Flask(__name__)
DATABASE = 'test.db'

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
r = recommend.SVDRecommender(get_db);

# Instantiate a random recommender.
#r = recommend.RandomRecommender(get_db)

#Sets up index route which will display index() function when route is visited.
#index() function calls render_template method(which knows to check templates folder) to return our index.html.
#methods enable us to POST and GET from the route (database).
@app.route('/', methods=['POST', 'GET'])
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    allBooks = c.fetchall()
    return render_template('index.html', allBooks = allBooks)


@app.route('/results', methods=['POST', 'GET'])
def results():
    bookResults = r.get()
    return render_template('results.html', bookResults = bookResults)

#Enables debug mode which displays errors on webpage.
if __name__ == "__main__":
    app.run(debug=True)
