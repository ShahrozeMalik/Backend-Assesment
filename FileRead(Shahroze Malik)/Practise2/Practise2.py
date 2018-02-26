from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FileInfo.sqlite3'


db = SQLAlchemy(app)
class FileInfo(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


@app.route('/')
def main():
    return render_template("FileUpload.html")


@app.route('/index')
def index():
    return render_template("FileUpload.html")


@app.route('/upload', methods=['POST'])
def upload():
    count = 0
    file = request.files['inputFile']
    data = file.readlines()
    for fullName in data:
        fullName = fullName.rstrip()
        fullName = fullName.decode("utf-8")
        str = fullName
        obj = FileInfo(str)
        db.session.add(obj)
        db.session.commit()
        name = fullName.split(" ")
        if(name[len(name)-1]=="siddique"):
            count+=1
    print(count)
    return '<h1>There are {} names which has last name of siddique</h1>'.format(count)


if __name__ == '__main__':
    app.run()
