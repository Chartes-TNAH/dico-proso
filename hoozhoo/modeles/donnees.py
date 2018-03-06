# fichier recevant les modèles de données pour l'application, hors données utilisateurs.

# ATTENTION
# Ici on utilise la variable "db", comme dans le cours. Il faut vérifier qu'elle est bien déclarée là où elle doit l'être (app.py ?).

class Person(db.Model):
    person_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    person_name = db.Column(db.Text)
    person_firstname = db.Column(db.Text)
    person_nickname = db.Column(db.Text)
    person_description = db.Column(db.Text, nullable=False)
    person_birthdate = db.Column(db.String(12))
    person_deathdate = db.Column(db.String(12))
    person_gender = db.Column(db.Text, nullable=False)
    person_external_id = db.Column(db.String(45))
# Jointure
    authorship_person = db.relationship("Authorship_person", back_populates="person")

class Relation_type(db.Model):
    relation_type_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    relation_type_name = db.Column(db.String(45), nullable=False)
    relation_type_code = db.Column(db.String(45), nullable=False)

class Authorship_person(db.Model):
    authorship_person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    authorship_person_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# Jointure
    authorship_person_user = db.Colum(db.Integer, db.ForeignKey('user.user_id'))
    authorship_person_person = db.Column(db.Integer, db.ForeignKey('person.person_id'))
# vérifier cette relation dans la table USER
    user = db.relationship("User", back_populates="authorship_person")
# vérifier cette relation dans la table Person
    person = db.relationship("Person", back_populates="authorship_person")
