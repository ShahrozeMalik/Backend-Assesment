from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TodayTask.db'


db = SQLAlchemy(app)


class Works(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    todo = db.Column(db.String(50))
    done = db.Column(db.Boolean)
    priority = db.Column(db.String(50))

    def __int__(self, todo, done, priority):
        self.todo = todo
        self.done = done
        self.priority = priority


@app.route('/')
def index():
    lists = Works.query.filter_by(done=False).order_by(Works.priority.desc()).all()
    return render_template('index.html', lists=lists)


@app.route('/GetItem', methods=['POST'])
def add():
    if request.method=="POST":
        obj = Works(todo=request.form['todoItem'], priority=request.form['priority'], done=False)
        db.session.add(obj)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/UpdateOrDelete', methods=['POST'])
def update():
    if request.form['submit'] == 'Mark as complete':
        id=request.form['on']
        list=Works.query.filter_by(id=int(id)).first()
        list.done=True
        db.session.commit()

    elif request.form['submit'] == 'Delete':
        id=request.form['on']
        obj=Works.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()