from flask import url_for
import datetime
# ATTENTION
# Ici on utilise la variable "db", comme dans le cours.
# Il faut vérifier qu'elle est bien déclarée là où elle doit l'être (dans app.py ?).
from .. app import db


class Link(db.Model):
    __tablename__ = "link"
    link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    link_person1_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_person2_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
# Jointure
    relation = db.relationship("Relation_type", back_populates="type_link")
    pers1 = db.relationship("Person", back_populates="link_pers1")
    pers2 = db.relationship("Person", back_populates="link_pers2")

class Authorship_link(db.Model):
    __tablename__ = "authorship_link"
    authorship_link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_link_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_link_link_id = db.Column(db.Integer, db.ForeignKey('link.link_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
    authorship_link_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    link_pers1 = db.relationship("Link", back_populates="pers1")
    link_pers2 =  db.relationship("Link", back_populates="pers2")

class Relation_type(db.Model):
    __tablename__ = "relation_type"
    relation_type_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    relation_type_name = db.Column(db.String(45), nullable=False)
    relation_type_code = db.Column(db.String(45), nullable=False)
# Jointure
    type_link = db.relationship("Link", back_populates="relation")

class Authorship_person(db.Model):
    __tablename__ = "authorship_person"
    authorship_person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    authorship_person_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# Jointure
    authorship_person_user_id = db.Colum(db.Integer, db.ForeignKey('user.user_id'))
    authorship_person_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    person = db.relationship("Person", back_populates="authorships_p")
    user_p = db.relationship("User", back_populates="authorship_person") # changer le nom de ce back_populates
