from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode

PERSONNES_PAR_PAGES = 3
from ..app import app, db
from ..modeles.donnees import Person, Link, Relation_type


def Json_404():
    response = jsonify({"erreur": "la requête a échoué"})
    response.status_code = 404
    return response


@app.route("/api/person/<int:identifier>")
def json_person(identifier):
    person = Person.query.get(identifier)
    return jsonify(person.person_to_json())


@app.route("/api/person")
def json_recherche():
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
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

    try:
        resultats = query.paginate(page=page, per_page=PERSONNES_PAR_PAGES)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            personne.person_to_json()
            for personne in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("json_recherche", _external=True) + "?" + urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("json_recherche", _external=True) + "?" + urlencode(arguments)

    response = jsonify(dict_resultats)
    return response
