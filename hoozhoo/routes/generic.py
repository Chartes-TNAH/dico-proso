from flask import render_template, request, flash, redirect
from ..app import app
from ..modeles.donnees import Person, Link
from ..modeles.utilisateurs import User


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
    personnes = Person.query.all()
    return render_template("pages/index.html", personnes=personnes)



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

@app.route("/modification/<int:identifier>", methods=["POST", "GET"])
#@login_required #désactivé pour le test
def modification (identifier):
    """
    route permettant de modifier un formulaire avec les données d'une personne
    :param identifier: identifiant numérique de la personne récupéré depuis la page notice
    """
    # renvoyer sur la page html les éléments de l'objet personne correspondant à l'identifiant de la route
    if request.method == "GET":
        personne_origine = Person.query.get(identifier)
        return render_template("pages/modification.html", personne_origine=personne_origine)

        # on récupère les données du formulaire modifié
    else:
        status, personneModifier= Person.modifier_person(
            id = identifier,
            nom = request.form.get("nom", None),
            prenom = request.form.get("prenom", None),
            surnom = request.form.get("surnom", None),
            description = request.form.get("description", None),
            date_naissance = request.form.get("date_naissance", None),
            date_deces = request.form.get("date_deces", None),
            genre = request.form.get("genre", None),
            id_externes = request.form.get("id_externes", None)
        )

        if status is True:
            flash("Modification réussie !", "success")
            return render_template ("pages/notice.html", unique=personneModifier, listLien=personneModifier.link_pers1)
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(personneModifier), "danger")
            personne_origine = Person.query.get(identifier)
            return render_template("pages/modification.html", personne_origine=personne_origine)


