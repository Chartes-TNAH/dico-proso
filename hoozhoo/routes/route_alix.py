from flask import render_template, request, flash, redirect


from .app import app, login
from .modeles.donnees import Place
from .modeles.utilisateurs import User
from .constantes import LIEUX_PAR_PAGE
from flask_login import login_user, current_user, logout_user


@app.route("/about")
def about():
    return render_template("pages/about.html")
