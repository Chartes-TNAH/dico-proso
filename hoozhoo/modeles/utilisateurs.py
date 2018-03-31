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
    author_person = db.relationship("Authorship_person", back_populates="user_person")
    author_link = db.relationship("Authorship_link", back_populates="user_link")

    @staticmethod
    def creer(login, email, nom, motdepasse):
	    """ Crée un compte utilisateur-rice. Retourne un tuple (booléen, User ou liste).
	    Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
	    Sinon, elle renvoie True suivi de la donnée enregistrée

	    :param login: Login de l'utilisateur-rice
	    :param email: Email de l'utilisateur-rice
	    :param nom: Nom de l'utilisateur-rice
	    :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)
            :param motdepasse-confirmation: Confirmation du mot de passe par l'utilisateur

	    """
	    erreurs = []
	    if not login:
	        erreurs.append("Le login fourni est vide")
	    if not email:
	        erreurs.append("L'email fourni est vide")
	    if not nom:
	        erreurs.append("Le nom fourni est vide")
	    if not motdepasse or len(motdepasse) < 6:
	        erreurs.append("Le mot de passe fourni est vide ou trop court")
            if not motdepasse-confirmation or motdepasse-confirmation != motdepasse:
                erreur.append("Le mot de passe fourni est différent du mot de passe initial")

	    # On vérifie que personne n'a utilisé cet email ou ce login
	    uniques = User.query.filter(
	        db.or_(User.user_email == email, User.user_login == login)
	    ).count()
	    if uniques > 0:
	        erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

	    # Si on a au moins une erreur
	    if len(erreurs) > 0:
	        return False, erreurs

	    # On crée un utilisateur
	    utilisateur = User(
	        user_name=nom,
	        user_login=login,
	        user_email=email,
	        user_password=generate_password_hash(motdepasse)
	    )

	    try:
	        # On l'ajoute au transport vers la base de données
	        db.session.add(utilisateur)
	        # On envoie le paquet
	        db.session.commit()

	        # On renvoie l'utilisateur
	        return True, utilisateur
	    except Exception as erreur:
	        return False, [str(erreur)]
