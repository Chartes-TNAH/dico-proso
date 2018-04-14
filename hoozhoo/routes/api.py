from flask import jsonify
# from urllib.parse import urlencode # à télécharger en requirements ?

from ..app import app
from ..modeles.donnees import Person, Link, Relation_type

def Json_404():
	response = jsonify({"erreur":"la requête a échoué"})
	response.status_code = 404
	return response

@app.route("/api/person/<int:identifier>")
def json_person(identifier):
	person = Person.query.get(identifier)
	return jsonify(person.person_to_json)