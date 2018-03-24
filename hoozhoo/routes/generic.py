from flask import render_template, request, flash, redirect
from ..app import app
from ..modeles.donnees import Person, Link
from ..modeles.utilisateurs import User

#variable à utiliser pour la pagination de la page recherche et index
PERSONNES_PAR_PAGES = 3

@app.route("/")
def debut():

    return "Hello"


@app.route("/a-propos")
def about():
    return render_template("pages/about.html")

@app.route("/index")
def index():
    """
    Route qui affiche la liste des personnes (Nom, prenom) de la base.
    """
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    titre="Index"
#creation de la pagination avec la methode .paginate qui remplace le .all dans la requête sur la base
    personnes = Person.query.order_by(Person.person_name).paginate(page=page, per_page= PERSONNES_PAR_PAGES)
    return render_template("pages/index.html", personnes=personnes, titre=titre)



@app.route("/person/<int:identifier>")
def notice(identifier):
    """
    Route qui affiche la notice descriptive de la personne
    :param identifier: identifiant numérique de la personne
    """
    personneUnique = Person.query.get(identifier)

    listLien = personneUnique.link_pers1

    return render_template("pages/notice.html", unique=personneUnique, listLien=listLien)

@app.route("/creer-lien", methods=["GET", "POST"])
#@login_required #désactivé pour le test
def creer_lien():
    """ route permettant à un utilisateur enregistré de créer un ou plusieurs liens entre des personnes existant dans la base
    """
    if request.method == "POST":
        # méthode statique create_link() à créer sous Link
        status, data = Link.create_link(
        link_person1=request.form.getlist("link_1_person[]", None),
        link_relation_type=request.form.getlist("link_relation_type[]", None),
        link_person2=request.form.getlist("link_2_person[]", None)
        )

        if status is True:
            flash("Création d'un nouveau lien réussie !", "success")
            return redirect("/creer-lien")
        else:
            flash("La création d'un nouveau lien a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
            return render_template("pages/creer_lien.html")

    else:
        return render_template("pages/creer_lien.html")