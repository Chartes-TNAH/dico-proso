from flask import url_for
import datetime
# ATTENTION
# Ici on utilise la variable "db", comme dans le cours.
# Il faut vérifier qu'elle est bien déclarée là où elle doit l'être (dans app.py ?).
from .. app import db


class Person(db.Model):
    __tablename__ = "person"
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
    authorships_p = db.relationship("Authorship_person", back_populates="person")
    link_pers1 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person1_id")
    link_pers2 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person2_id")

class Relation_type(db.Model):
    __tablename__ = "relation_type"
    relation_type_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    relation_type_name = db.Column(db.String(45), nullable=False)
    relation_type_code = db.Column(db.String(45), nullable=False)
    relation_type_first_snap = db.Column(db.String(45))
    relation_type_second_snap = db.Column(db.String(45))
    relation_type_third_snap = db.Column(db.String(45))
    relation_type_fourth_snap = db.Column(db.String(45))
# Jointure
    type_link = db.relationship("Link", back_populates="relations")

class Link(db.Model):
    __tablename__ = "link"
    link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    link_person1_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_person2_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
# Jointure
    relations = db.relationship("Relation_type", back_populates="type_link")
    person1 = db.relationship("Person", foreign_keys=[link_person1_id])
    person2 = db.relationship("Person", foreign_keys=[link_person2_id])
    authorships_l = db.relationship ("Authorship_link", back_populates="link_link")

    @staticmethod
    def create_link(link_person1, link_relation_type, link_person2):
        """ Crée un nouveau lien, retourn un tuple (booléen, lien ou liste).
        S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de la donnée enregistrée.
        :param link_person1: nom de la personne 1
        :param link_person2: nom de la personne 2
        :param link_relation_type: nom de la relation (modele SNAP)
        """

        errors = []

        # On vérifie que les champs sont remplis pour chaque ligne
        if not link_person1:
            errors.append(" - le champ 'Personne 1' n'a pas été rempli")
        if not link_relation_type:
            errors.append(" - le champ 'Relation' n'a pas été rempli")
        if not link_person2:
            errors.append(" - le champ 'Personne 2' n'a pas été rempli")
        if link_person1 == link_person2:
            errors.append(" - les champs 'Person 1' et 'Person 2' sont identiques")
        if len(errors) > 0:
            return False, errors

        # On vérifie les ID sont valides
        person1 = Person.query.filter(Person.person_id == link_person1).all()
        person2 = Person.query.filter(Person.person_id == link_person2).all()

        if len(person1) == 0:
            errors.append("'Person 1' n'existe pas")
        if len(person2) == 0:
            errors.append("'Person 2' n'existe pas")

        # On récupère l'id de la relation dans la table Relation_type :
        relation = Relation_type.query.filter(Relation_type.relation_type_name == link_relation_type).all()

        # On vérifie que la requête d'id de relation a bien fonctionné
        if len(relation) == 0:
            errors.append("Erreur de lien")

        # Deuxième niveau d'interruption si erreurs.
        if len(errors) > 0:
            return False, errors

        # On récupère l'id associé au lien.
        u_relation = relation[0]
        link_relation_type = u_relation.relation_type_id

        # On vérifie que le lien n'existe pas déjà
        uniques = Link.query.filter(
            db.and_(Link.link_person1_id == link_person1, Link.link_person2_id == link_person2, Link.link_relation_type_id == link_relation_type)
        ).count()
        if uniques > 0:
            erreurs.append("Le lien existe déjà")

        # Si on a au moins une erreur :
        if len(errors) > 0:
            return False, errors

        # Sinon, on crée un nouveau lien

        created_link = Link(
            link_person1_id=link_person1,
            link_relation_type_id=link_relation_type,
            link_person2_id=str(link_person2)
            )

        try:
        # Phase de création du lien :
            db.session.add(created_link)
            db.session.commit()

        # Renvoie d'informations vers l'utilisateur :
            return True, created_link

        except Exception as error_creation:
            return False, [str(error_creation)]

class Authorship_link(db.Model):
    __tablename__ = "authorship_link"
    authorship_link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_link_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_link_link_id = db.Column(db.Integer, db.ForeignKey('link.link_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
    authorship_link_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# Jointure
    user_link = db.relationship("User", back_populates="author_link")
    link_link = db.relationship("Link", back_populates="authorships_l")

class Authorship_person(db.Model):
    __tablename__ = "authorship_person"
    authorship_person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    authorship_person_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    authorship_person_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_person_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
# Jointure
    person = db.relationship("Person", back_populates="authorships_p")
    user_person = db.relationship("User", back_populates="author_person")
