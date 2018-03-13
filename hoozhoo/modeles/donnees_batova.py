from flask import url_for
import datetime

from .. app import db


class Link(db.Model):
    __tablename__ = "link"
    link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    link_person1_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_person2_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
    authorlink = db.relationship("Authorship_link", back_populates="link")
##### Je ne suis pas sûre que c'est bien ça
    person1 = db.relationship("Person", back_populates="link1")
    person2 = db.relationship("Person", back_populates="link2")
    relations = db.relationship("Relation_type", back_populates="link")

##### FOR Person : add these lines
##### Je ne suis pas sûre

    link1 = db.relationship("Link", back_populates="person1")
    link2 = db.relationship("Link", back_populates="person1")

##### FOR relation_type :::

    link = db.relationship("Link", back_populates="relations")

class Authorship_link(db.Model):
    __tablename__ = "authorship_link"
    authorship_link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_link_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_link_link_id = db.Column(db.Integer, db.ForeignKey('link.link_id'))
    authorship_link_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    link = db.relationship("Link", back_populates="authorlink")
    user = db.relationship("User", back_populates="authorlink")

##### FOR Auhorship_person : add this line

    user = db.relationship("User", back_populates="authorperson")
