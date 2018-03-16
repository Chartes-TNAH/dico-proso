from flask import render_template
from ..app import app
from ..modeles.donnees import Person
from ..modeles.utilisateurs import User


@app.route("/index")
def index():
    """
    Route qui affiche la liste des personnes (Nom, prenom) de la base.
    """
    personnes = Person.query.order_by(Person.person_id).limit(5).all()
    return render_template("pages/index.html", personnes=personnes)



@app.route("/person/<int:identifier>")
def person(identifier):
    """
    Route qui affiche la notice descriptive de la personne
    :param identifier: identifiant numérique de la personne
    """
    personne = Person.query.get(identifier)
    return render_template("pages/notice.html", personne=personne)



