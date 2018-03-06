from flask import url_for
import datetime

from .. app import db


class Link(db.Model):
    __tablename__ = "link"
    link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    link_person1_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_person2_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))

class Authorship_link(db.Model):
    __tablename__ = "authorship_link"
    authorship_link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_link_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_link_link_id = db.Column(db.Integer, db.ForeignKey('link.link_id'))
    link_relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.relation_type_id'))
    authorship_link_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
