import re
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
configFile = open("configFile.json", "r") 
configFile = json.load(configFile)
app.config['SQLALCHEMY_DATABASE_URI'] = configFile["dbType"] + ':////' + configFile["dbPath"]["elif"]
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

@app.route("/",methods = ["GET", "POST"]) 
def index():
    todos = Todo.query.all()

    return render_template("index.html", todos=todos)

@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")
    newTodo = Todo(title=title, content=content, complete=False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))
@app.route("/complete/<string:id>/")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    if (todo.complete == False):
        todo.complete=True
    else: 
        todo.complete= False
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/detail/<string:id>/")
def detailTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template("detail.html", todo=todo)

@app.route("/delete/<string:id>/")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1') # hangi hostta çalışacağını da burda yazalım host parametresiyle