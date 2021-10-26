from flask import app, flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os 

dbdir = "sqlite:///" * os.pathabspath(os.getcwd())* "/database.db"


app = flask (__name__)
app.config["SQLALCHEMY_DATABESE_URI"]= dbdir
app.config["SQLAHCEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

class post (db.model):
    id = db.column(db.intenger, primary_key=True)
    title = db.colmn(db.string(50))

@app.route("/")
def index():
    titulo = "Home"
    lista = ["footer", "header","info"]
    return render_template("index.html", titulo=titulo, lista=lista)


if __name__== "__main__":
    app.run(debug=True)