from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. app import db, login


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
# Jointure
    authorships_person = db.relationship("Authorship_person", back_populates="user_p")

# AJOUTER  LES METHODES STATIQUES
