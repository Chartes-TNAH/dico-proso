from flask import render_template
from ..app import app
from ..modeles.donnees import Person
from ..modeles.utilisateurs import User


@app.route("/")
def debut():

    return "Hello"


@app.route("/a-propos")
def about():
    return render_template("pages/about.html")

