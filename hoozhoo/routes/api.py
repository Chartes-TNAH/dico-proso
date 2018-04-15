from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode


from ..app import app, db
from ..modeles.donnees import Person, Link, Relation_type


def Json_404():
    response = jsonify({"erreur": "la requête a échoué"})
    response.status_code = 404
    return response


@app.route("/api/person/<int:identifier>")
def json_person(identifier):
    person = Person.query.get(identifier)
    if not person:
        return Json_404()
    else: 
        return jsonify(person.person_to_json())


@app.route("/api/person")
def json_recherche():
    motclef = request.args.get("q", None)

    if motclef :
        query = Person.query.filter(db.or_(
            Person.person_name.like("%{}%".format(motclef)),
            Person.person_firstname.like("%{}%".format(motclef)),
            Person.person_nickname.like("%{}%".format(motclef)),
            Person.person_nativename.like("%{}%".format(motclef)),
            Person.person_country.like("%{}%".format(motclef)),
            Person.person_language.like("%{}%".format(motclef)),
            Person.person_occupations.like("%{}%".format(motclef)),
            Person.person_description.like("%{}%".format(motclef))))
    else:
        query = Person.query


# vérification de la présence d'un résultat : s'il n'y en a pas, retourne une erreur 404
    resultats = query.all()

    if len(resultats) == 0 :
    	return Json_404()
    else :
    	dict_resultats = {
	        "resultats": [
	            personne.person_to_json()
	            for personne in resultats
        ]
    }

    response = jsonify(dict_resultats)
    return response
