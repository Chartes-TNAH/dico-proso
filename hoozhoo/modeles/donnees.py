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
    person_country = db.Column(db.Text)
    person_language = db.Column(db.Text)
    person_occupations = db.Column(db.Text)
    person_nativename = db.Column(db.Text)
    person_external_id = db.Column(db.String(45))
# Jointure
    authorships_p = db.relationship("Authorship_person", back_populates="person")
    link_pers1 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person1_id")
    link_pers2 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person2_id")

    @staticmethod
    def create_person(nom, prenom, surnom, description, date_naissance, date_deces, genre, id_externes):
        # on vérifie qu'au moins un des trois champs (nom, prénom et surnom) est rempli ainsi que celui de la description qui est obligatoire
        errors = []
        if not (nom or prenom or surnom):
            errors.append("Un des trois champs (nom, prénom, surnom) est obligatoire")
        # vérifier que le champ description est bien rempli
        if not description:
            errors.append("Le champ description est obligatoire")
        # si on a au moins une erreur
        if len(errors) > 0:
            return False, errors

        # vérifier si la personne existe
        personne = Person.query.filter(db.and_(Person.person_name == nom, Person.person_firstname == prenom,
                                               Person.person_nickname == surnom)).count()
        if personne > 0:
            errors.append("La personne est déjà inscrite dans la base de données")

        # Si on a au moins une erreur
        if len(errors) > 0:
            return False, errors

        # Sinon, on crée une nouvelle personne dans la table Person
        created_person = Person(
            person_name=nom,
            person_firstname=prenom,
            person_nickname=surnom,
            person_description=description,
            person_birthdate=date_naissance,
            person_deathdate=date_deces,
            person_gender=genre,
            person_external_id=id_externes
        )

        try:
            # création de la nouvelle personne :
            db.session.add(created_person)
            db.session.commit()

            # Renvoie d'informations vers l'utilisateur :
            return True, created_person

        except Exception as error_creation:
            return False, [str(error_creation)]

    @staticmethod
    def modifier_person (id, nom, prenom, surnom, description, date_naissance, date_deces, genre, id_externes):
        """ Modifie la notice d'une personne, ....à compléter
               """
        erreurs=[]
        if not (nom or prenom or surnom):
            erreurs.append("Un des trois champs (nom, prénom, surnom) est obligatoire")
        if not description:
            erreurs.append("Le champ description est obligatoire")
        if not id_externes:
            erreurs.append("L'identifiant Wikidata est obligatoire")
        if len(erreurs) > 0:
            return False, erreurs

        # récupérer une personne dans la base
        personne = Person.query.get(id)

        #vérifier que l'utilisateur modifie au moins un champ

        if personne.person_name == nom and personne.person_firstname == prenom and personne.person_nickname == surnom and personne.person_description.strip() == description.strip() and personne.person_birthdate == date_naissance and personne.person_deathdate == date_deces and personne.person_gender == genre and personne.person_external_id == id_externes:
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs

        #vérifier que la taille des caractères insérés (nom, prenonm, surnon, date, ID externes) ne dépasse pas la limite acceptée par mysql

        if len(nom) > 255 or len(prenom) > 255 or len(surnom) > 255 :
            erreurs.append("La taille des caractères du nom, ou du prénom ou du surnon a été dépassée")
        if len(erreurs) > 0:
            return False, erreurs

        if len(date_naissance) > 12 or len(date_deces) > 12 :
            erreurs.append("La taille des caractères des dates a été dépassée")
        if len(erreurs) > 0:
            return False, erreurs

        if len(id_externes) > 45 :
            erreurs.append("La taille des caractères des dates a été dépassée")
        if len(erreurs) > 0:
            return False, erreurs

        #vérifier que l'ID Wikidata commence par Q
        if id_externes[0] != "Q" :
            erreurs.append("L'ID Wikidata doit commencer par 'Q'")
        if len(erreurs) > 0:
            return False, erreurs

        else:
            # mise à jour de la personne
            personne.person_name=nom
            personne.person_firstname=prenom
            personne.person_nickname=surnom
            personne.person_description=description
            personne.person_birthdate=date_naissance
            personne.person_deathdate=date_deces
            personne.person_gender=genre
            personne.person_external_id=id_externes

        try:
            #ajout dans la base de données
            db.session.add(personne)
            db.session.commit()
            return True, personne

        except Exception as error_modification:
            return False, [str(error_modification)]


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
        """ Crée un nouveau lien, retourne un tuple (booléen, liste).
        S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi d'une liste de données enregistrées.
        :param link_person1: liste de noms de la personne 1
        :param link_person2: liste de noms de la personne 2
        :param link_relation_type: liste d'id numérique de relation, ou bien "choisir"
        """
        print("TEST")
        print(link_person1)
        print(link_person2)
        print(link_relation_type)

        errors = []

        # On vérifie que les champs de toutes les lignes sont remplis
        if not( (len(link_person1) == len(link_person2)) and (len(link_person1) == len(link_relation_type)) and (len(link_person2) == len(link_relation_type)) ):
            errors.append("certains champs sont vides")
        if len(errors) > 0:
            return False, errors

        # Calcul du nombre d'itérations nécessaire pour la boucle
        loop = len(link_person1)
        # On vérifie qu'aucune ligne n'est identique à une autre
        triplets = []
        repeat = 0
        for row in range (0, loop):
            triplet = (link_person1[row], link_relation_type[row], link_person2[row])
            for trio in triplets:
                if triplet == trio:
                    repeat += 1
            triplets.append(triplet)
        if repeat > 0:
            errors.append("certains liens à créer sont identiques")
        # on vérifie que le type de relation a bien été séléctionné, et que les champs pers1 et pers2 ne sont pas identiques:
        for row in range (0, loop):
            if link_relation_type[row] == 'Choisir':
                errors.append("aucun type de relation n'a été sélectionné, ligne " + str(row +1))
            if link_person1[row] == link_person2[row]:
                errors.append("les champs 'Personne 1' et 'Personne 2' sont identiques, ligne " + str(row +1))
        if len(errors) > 0:
            return False, errors

        # On vérifie les ID sont valides
        for row in range (0, loop):
            person1 = Person.query.filter(Person.person_id == link_person1[row]).count()
            person2 = Person.query.filter(Person.person_id == link_person2[row]).count()
            if person1 == 0:
                errors.append(link_person1[row] +" n'existe pas, ligne " + str(row +1))
            if person2 == 0:
                errors.append(link_person2[row] +" n'existe pas, ligne " + str(row +1))
        if len(errors) > 0:
            return False, errors

        # On vérifie que le lien n'existe pas déjà
        for row in range (0, loop):
            uniques = Link.query.filter(
                db.and_(Link.link_person1_id == link_person1[row], Link.link_person2_id == link_person2[row], Link.link_relation_type_id == link_relation_type[row])
                ).count()
            if uniques > 0:
                errors.append("le lien existe déjà")
        if len(errors) > 0:
            return False, errors

        # On itère à nouveau pour créer un lien :
        # la liste created_link va récupérer l'ensemble des données enregistrées
        created_link = []
        for row in range (0, loop):
            created_link.append(
                Link(
                    link_person1_id=link_person1[row],
                    link_relation_type_id=str(link_relation_type[row]),
                    link_person2_id=link_person2[row]
                    )
                )

        try:
            for row in range (0, loop):
                # Phase de création du lien :
                db.session.add(created_link[row])
                db.session.commit()
            # Renvoie d'informations vers l'utilisateur :
            return True, created_link

        # Sinon renvoie l'erreur vers l'utilisateur :
        except Exception as error_creation:
            return False, [str(error_creation)]


    @staticmethod
    def modifier_link(id, link_person1_id, link_relation_type, link_person2_id):
        """
        Modifie un lien dans la base de donnée, retourne un tuple (booléen, liste ou objet).
        S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de la donnée enregistrée.
        :param id : un identifiant numérique du lien
        :param link_person1_id : un identifiant numérique de la personne 1
        :param link_relation_type : une chaine de caractère correspondant à un type de relation 
        :param link_person2_id : un identifiant numérique de la personne 2
        """

        errors = []
        
        # on vérifie que tous les paramètres sont complétés : 
        if not id:
            errors.append("erreur d'identification du lien à éditer")
        if not link_person1_id:
            errors.append("le champ personne 1 est vide")
        if not link_person2_id:
            errors.append("le champ personne 2 est vide")
        if not link_relation_type:
            errors.append("aucune relation n'a été spécifiée")
        # on vérifie que personne 1 et personne 2 ne sont pas identiques 
        if link_person1_id == link_person2_id:
            errors.append("personne 1 et personne 2 ne peuvent pas être identiques")

        # s'il y a des erreurs, on interrompt le processus
        if len(errors) > 0:
            return False, errors

        # on récupère l'id du type de relation 
        relation_id = Relation_type.query.filter(Relation_type.relation_type_name == link_relation_type).all()
        relation_type = relation_id[0]
        id_relation = relation_type.relation_type_id

        # on récupère le lien dans la base 
        origin_link = Link.query.get(id)
        # on vérifie qu'une modification a été effectuée : 
        if origin_link.link_person1_id == link_person1_id and origin_link.link_person2_id == link_person2_id and origin_link.link_relation_type_id == id_relation:
            errors.append("Aucune modification n'a été réalisée")
        if len(errors) > 0:
            return False, errors

        # on vérifie que le lien n'existe pas déjà
        uniques = Link.query.filter(
            db.and_(Link.link_id != id, Link.link_person1_id == link_person1_id, Link.link_person2_id == link_person2_id, Link.link_relation_type_id == id_relation)
            ).count()
        if uniques > 0:
            errors.append("le lien modifié existe déjà")

        if len(errors) > 0:
            return False, errors

        # mise à jour du lien
        origin_link.link_person1_id=link_person1_id
        origin_link.link_person2_id=link_person2_id
        origin_link.link_relation_type_id=id_relation

        try:
            # ajout de la mise à jour du lien dans la base de données
            db.session.add(origin_link)
            db.session.commit()
            return True, origin_link

        except Exception as error_modification:
            return False, [str(error_modification)]

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
