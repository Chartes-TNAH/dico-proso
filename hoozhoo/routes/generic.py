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
    # récupérer l'objet correspondant à l'identifiant de la route pour retourner l'objet personne qui doit être modifié
    if request.method == "GET":
        personne_origine = Person.query.get(identifier)
        return render_template("pages/modification.html", personne_origine=personne_origine)

        # on récupère les données du formulaire
    else:
        personne_corriger = request.form.get("nomlieu", None)
    if lieu_corriger:
        # je récupère l'objet correspondand au lieu d'origine en faisant une requête get dans la base de données
        lieu_origine = Place.query.get(nr_place)
        # je fais une nouvelle affectation
        lieu_origine.place_nom = lieu_corriger

        db.session.add(lieu_origine)
        db.session.commit()

        flash("Modification effectuée.", "success")

    return render_template("pages/place.html", lieu=lieu_origine)

