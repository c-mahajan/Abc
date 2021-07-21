from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

''' SQLAlchemy COnfigurations '''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' #Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

''' Model Definition '''
class Todo(db.Model):
    sr_no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sr_no} - {self.title}"

''' Controllers '''
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc=desc)                   #Create Operation
        db.session.add(todo)
        db.session.commit()

    alltodos = Todo.query.all()                                 #Read All Operation
    return render_template('index.html', todos=alltodos)
    
@app.route('/update/<int:sr_no>', methods=['GET', 'POST'])      #Update Operation
def update(sr_no):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sr_no>')                               #Delete Operation
def delete(sr_no):
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True, port=8000)
