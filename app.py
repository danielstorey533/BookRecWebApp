#Enter 'python app.py' to launch webserver in terminal.

#Commands used for launching db:
#from app import db (after writing py) - imports our db to shell
#db.create_all()
#exit()




#Imports flask from Flask class -- Flask is a web framework for Python.
#Flask uses Jinja for templates; which is a web template engine.
from flask import Flask, render_template, url_for, request, redirect
#SQLAlchemy is the Python SQL toolkit - used for connecting to our book and ratings sql
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Sets up the app and database. Enter 'python app.py' to launch in terminal.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Database class and rules
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#Sets up index route which will display index() function when route is visited.
#index() function calls render_template method(which knows to check templates folder) to return our index.html.
#methods enable us to POST and GET from the route (database).
@app.route('/', methods=['POST', 'GET'])
def index():

    #If POST request is sent to route, execute statement
    if request.method == 'POST':
        #Creates new task from input then tries to commit to database
        #then redirects to index.html
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            #error message if commit does not execute
            return 'There was an issue adding task'

    else:
        #Displays all db tasks based on date created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

#Enables debug mode which displays errors on webpage.
if __name__ == "__main__":
    app.run(debug=True)