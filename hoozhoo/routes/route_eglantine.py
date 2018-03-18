from flask import render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user

from ..app import app, login
from ..constantes import LIEUX_PAR_PAGE
from ..modeles.donnees import Place
from ..modeles.utilisateurs import User



@app.route("/register", methods=["GET", "POST"])
def inscription():

    
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")
