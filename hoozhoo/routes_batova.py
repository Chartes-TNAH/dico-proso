@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions des utilisateurs
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    if request.method == "POST":
        user = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("password", None)
        )
        if user:
            flash("Connexion effectuée", "success")
            login_user(user)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "danger")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'
