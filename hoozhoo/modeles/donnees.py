from flask import url_for
import datetime
from flask_login import current_user
from .. app import db


##############################################################################################################
#                                                 PERSON                                                     #
##############################################################################################################

class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    person_name = db.Column(db.Text)
    person_firstname = db.Column(db.Text)
    person_nickname = db.Column(db.Text)
    person_nativename = db.Column(db.Text)
    person_country = db.Column(db.Text)
    person_language = db.Column(db.Text)
    person_birthdate = db.Column(db.String(12))
    person_deathdate = db.Column(db.String(12))
    person_gender = db.Column(db.Text, nullable=False)
    person_occupations = db.Column(db.Text)
    person_description = db.Column(db.Text, nullable=False)
    person_external_id = db.Column(db.String(12), nullable=False)
# Jointure
    authorships_p = db.relationship("Authorship_person", back_populates="person")
    link_pers1 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person1_id")
    link_pers2 = db.relationship("Link", primaryjoin="Person.person_id==Link.link_person2_id")

    @staticmethod
    def create_person(nom, prenom, surnom, nom_languematernelle, pays_nationalite, langues, date_naissance, date_deces, fonctions_occupations, description, genre, id_externes):
        # on vérifie qu'au moins un des trois champs (nom, prénom et surnom) est rempli ainsi que celui de la description qui est obligatoire
        errors = []
        if not (nom or prenom or surnom):
            errors.append("Un des trois champs (nom, prénom, surnom) est obligatoire")
        # vérifier que le champ genre est bien coché
        if not genre:
            errors.append("Le champ genre est obligatoire")
        # vérifier que le champ description est bien rempli
        if not description:
            errors.append("Le champ description est obligatoire")
        # vérifier que le champ wikidata id est bien rempli
        if not id_externes:
            errors.append("L'identifiant Wikidata est obligatoire")
        # si on a au moins une erreur
        if len(errors) > 0:
            return False, errors

        #vérifier que la taille des caractères insérés (nom, prenonm, surnom) ne dépasse pas la limite acceptée par mysql
        if len(nom) > 255 or len(prenom) > 255 or len(surnom) > 255 :
            errors.append("La taille des caractères du nom, ou du prénom ou du surnon a été dépassée")
        if len(errors) > 0:
            return False, errors

        #vérifier que la taille des caractères insérés (date) ne dépasse pas la limite acceptée par mysql
        if len(date_naissance) > 12 or len(date_deces) > 12:
            errors.append("La taille des caractères des dates a été dépassée")
        if len(errors) > 0:
            return False, errors

        #vérifier que la taille des caractères insérés (wikidata id) ne dépasse pas la limite acceptée par mysql
        if len(id_externes) > 12 :
            errors.append("La taille des caractères du champs Wikidata ID a été dépassée")
        if len(errors) > 0:
            return False, errors

        #vérifier que l'ID Wikidata commence par Q
        if id_externes[0] != "Q" :
            errors.append("L'ID Wikidata doit commencer par 'Q'")
        if len(errors) > 0:
            return False, errors

        # vérifier si la personne existe
        personne = Person.query.filter(db.and_(Person.person_name == nom, Person.person_firstname == prenom,
                                               Person.person_nickname == surnom)).count()
        if personne > 0:
            errors.append("La personne est déjà inscrite dans la base de données")

        # vérifier si l'ID wikidata existe déjà 
        personne = Person.query.filter(Person.person_external_id == id_externes).count()

        if personne > 0:
            errors.append("L'identifiant Wikidata est déjà utilisé")

        # Si on a au moins une erreur
        if len(errors) > 0:
            return False, errors


        # Sinon, on crée une nouvelle personne dans la table Person
        created_person = Person(
            person_name=nom,
            person_firstname=prenom,
            person_nickname=surnom,
            person_nativename=nom_languematernelle,
            person_country=pays_nationalite,
            person_language=langues,
            person_birthdate=date_naissance,
            person_deathdate=date_deces,
            person_gender=genre,
            person_occupations=fonctions_occupations,
            person_description=description,
            person_external_id=id_externes
        )

        try:
            # création de la nouvelle personne :
            db.session.add(created_person)
            db.session.commit()

            # Création d'un log dans authorship_person
            creation = Person.query.filter(Person.person_external_id == id_externes).one()
            authorship_person=Authorship_person.authorship(
                updated=creation
                )
            # Renvoie d'informations vers l'utilisateur :
            return True, created_person

        except Exception as error_creation:
            return False, [str(error_creation)]

    @staticmethod
    def modifier_person (id, nom, prenom, surnom, nom_naissance, nationalite, langues, description, date_naissance, date_deces, fonctions, genre, id_externes):
        """ Modifie les informations de la notice d'une personne
        :param id: l'identifiant de la personne
        :type id: int
        :param nom : nom de la personne
        :param prenom : prénom de la personne
        :param surnom : surnom de la personne
        :param nom_naissance : nom d'origine de la personne
        :param nationalite : Pays de nationalité de la personne
        :param langues : langues utilisées par la personne
        :param description : description de la personne
        :param date_naissance : date de naissance de la personne
        :param date_deces : date de déces de la personne
        :param fonctions : fonctions/occupations de la personne
        :param genre : sexe de la personne
        :param id_externes : identifiant Wikidata
        :type nom, prenom, surnom, nom_naissance, nationalite, langues, description, date_naissance, date_deces, fonctions, genre, id_externes: str

        returns : Tuple (booléen, liste/objet).
        S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet mis à jour (ici personne).

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

        if personne.person_name == nom \
                and personne.person_firstname == prenom \
                and personne.person_nickname == surnom \
                and personne.person_description == description \
                and personne.person_birthdate == date_naissance \
                and personne.person_deathdate == date_deces \
                and personne.person_gender == genre \
                and personne.person_external_id == id_externes \
                and personne.person_nativename == nom_naissance \
                and personne.person_country == nationalite \
                and personne.person_language == langues \
                and personne.person_occupations == fonctions:
            erreurs.append("Aucune modification n'a été réalisée")

        if len(erreurs) > 0:
            return False, erreurs

        #vérifier que la taille des caractères insérés (nom, prenonm, surnon, date, ID externes) ne dépasse pas la limite acceptée par mysql

        if len(nom) > 255 or len(prenom) > 255 or len(surnom) > 255 :
            erreurs.append("La taille des caractères du nom, ou du prénom ou du surnon a été dépassée")

        if len(date_naissance) > 12 or len(date_deces) > 12 :
            erreurs.append("La taille des caractères des dates a été dépassée")

        if len(id_externes) > 12 :
            erreurs.append("La taille des caractères du champs Wikidata ID a été dépassée")

        #vérifier que l'ID Wikidata commence par Q
        if id_externes[0] != "Q" :
            erreurs.append("L'ID Wikidata doit commencer par 'Q'")
        if len(erreurs) > 0:
            return False, erreurs

        else:
            # mise à jour de la personne
            personne.person_name = nom
            personne.person_firstname = prenom
            personne.person_nickname = surnom
            personne.person_description = description
            personne.person_birthdate = date_naissance
            personne.person_deathdate = date_deces
            personne.person_gender = genre
            personne.person_external_id = id_externes
            personne.person_nativename = nom_naissance
            personne.person_country = nationalite
            personne.person_language = langues
            personne.person_occupations = fonctions

        try:
            #ajout dans la base de données
            db.session.add(personne)
            db.session.commit()

            # creation d'un log dans authorship_person
            authorship_person=Authorship_person.authorship(
                updated=Person.query.get(id)
                )
            # Renvoie d'informations vers l'utilisateur :
            return True, personne

        except Exception as error_modification:
            return False, [str(error_modification)]

    @staticmethod
    def supprimer_personne(id_personne):
        """
        Fonction qui supprime la notice
        :param id_personne: l'identifiant de la personne à récupérer dans l'adresse de la notice
        :type id_personne: int
        :returns : Booleens
        """
        #récupération de l'objet personne
        personneUnique = Person.query.get(id_personne)

        #récupération des liens ou uniquePersonne est la personne 1
        listLien1 = personneUnique.link_pers1
        # récupération des liens ou uniquePersonne est la personne 2
        listLien2 = personneUnique.link_pers2

        for lien in listLien1:
            Authorship_link.delete_logs(
                id_link=lien.link_id
                )
            db.session.delete(lien)
            db.session.commit()
        for lien in listLien2:
            Authorship_link.delete_logs(
                id_link=lien.link_id
                )
            db.session.delete(lien)
            db.session.commit()

        Authorship_person.delete_logs(
            id_person=id_personne
            )
        db.session.delete(personneUnique)
        db.session.commit()


    def person_to_json(self):
        """
        Fonction qui transforme les informations sur une personne en un dictionnaire pour un export en JsonLD via l'API
        :return:
        """

        dico = {
            "@context": [
                "https://schema.org/docs/jsonldcontext.json",
                "http://xmlns.com/foaf/context",
                {"snap": "http://data.snapdrgn.net/ontology/snap"} ],

                "@type": "person",
                "@id": url_for("notice", identifier=self.person_id, _external=True),
                "schema:familyName": self.person_name,
                "schema:givenName": self.person_firstname,
                "foaf:surname": self.person_nickname,
                "schema:gender": self.person_gender,
                "schema:description": self.person_description,
                "schema:sameAs": "https://www.wikidata.org/wiki/" + self.person_external_id,
                # "nom dans la langue de la personne": self.person_nativename,
                "schema:birthDate": self.person_birthdate,
                "schema:deathDate": self.person_deathdate,
                "schema:nationality": self.person_country,
                # "langues parlées, écrites ou signées": self.person_language,
                "schema:jobTitle": self.person_occupations,
                "snap:#link-with": [
                lien.link_to_json()
                for lien in self.link_pers1
            ]

            }
        return dico

##############################################################################################################
#                                            RELATION_TYPE                                                   #
##############################################################################################################

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


##############################################################################################################
#                                                    LINK                                                    #
##############################################################################################################

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
                # Création d'un log dans authorship_link
                creation = Link.query.filter(
                db.and_(Link.link_person1_id == link_person1[row], Link.link_person2_id == link_person2[row], Link.link_relation_type_id == link_relation_type[row])
                ).one()
                authorship_link=Authorship_link.authorship_l(
                    updated=creation
                    )
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
        :param link_relation_type : un identifiant numérique du type de relation  
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
        if len(errors) > 0:
            return False, errors

        exist = Person.query.get(link_person2_id)
        if not exist:
            errors.append(link_person2_id + " n'est pas un identifiant valide")
        if len(errors) > 0:
            return False, errors

        # on récupère le lien original dans la base 
        origin_link = Link.query.get(id)

        # on vérifie que le lien n'existe pas déjà
        uniques = Link.query.filter(
            db.and_(Link.link_id != id, Link.link_person1_id == link_person1_id, Link.link_person2_id == link_person2_id, Link.link_relation_type_id == link_relation_type)
            ).count()
        if uniques > 0:
            errors.append("le lien modifié existe déjà")
        if len(errors) > 0:
            return False, errors

        # mise à jour du lien
        origin_link.link_person1_id=link_person1_id
        origin_link.link_person2_id=link_person2_id
        origin_link.link_relation_type_id=link_relation_type

        try:
            # ajout de la mise à jour du lien dans la base de données
            db.session.add(origin_link)
            db.session.commit()

            # Création d'un log dans authorship_link
            creation = Link.query.get(id)
            authorship_link=Authorship_link.authorship_l(
                updated=creation
                )
            return True, origin_link

        except Exception as error_modification:
            return False, [str(error_modification)]

    @staticmethod
    def delete_link(link_id):
        """
        Supprime un lien dans la base de données, retourne un booléen : True si la suppression a réussi, sinon False.
        :param link_id : un identifiant numérique du lien
        """

        lien = Link.query.get(link_id)

        try:
            Authorship_link.delete_logs(
                id_link=link_id
                )
            db.session.delete(lien)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False

    def link_to_json (self):
        """
        Fonction qui retourne un dictionnaire à partir des éléments des la classe Link pour un export en JSON via l'API
        """

        #imbrication des différents niveaux de relation vers la personne
        bond = []
        bond_5 = []
        bond_4 = []
        bond_3 = []
        bond_2 = []

        bond_5.append("snap:"+self.relations.relation_type_code)
        if self.relations.relation_type_fourth_snap:
            bond_4.append("snap:"+self.relations.relation_type_fourth_snap)
        if self.relations.relation_type_third_snap:
            bond_3.append("snap:"+self.relations.relation_type_third_snap)
        if self.relations.relation_type_second_snap:
            bond_2.append("snap:"+self.relations.relation_type_second_snap)

        if len(bond_4) == 1:
            bond_4.append(bond_5)
            bond_3.append(bond_4)
            bond_2.append(bond_3)
            bond = bond_2
        elif len(bond_3) == 1:
            bond_3.append(bond_5)
            bond_2.append(bond_3)
            bond = bond_2
        elif len(bond_2) == 1:
            bond_2.append(bond_5)
            bond = bond_2
        else:
            bond = bond_5
            
        return {
                    "@id": url_for("notice", identifier=self.person2.person_id, _external=True),
                    "schema:familyName": self.person2.person_name,
                    "schema:givenName": self.person2.person_firstname,
                    "foaf:surname": self.person2.person_nickname,
                    "schema:gender": self.person2.person_gender,
                    "schema:description": self.person2.person_description,
                    "schema:identifier": self.person2.person_external_id,
                    "schema:birthDate": self.person2.person_birthdate,
                    "schema:deathDate": self.person2.person_deathdate,
                    "schema:nationality": self.person2.person_country,
                    "schema:jobTitle": self.person2.person_occupations,
                    "snap:#Bond": bond
            }


    def class_snap(self):
        dico_snap = []
        dico_snap.append(self.relations.relation_type_first_snap)
        if not(self.relations.relation_type_second_snap == ""):
            dico_snap.append(self.relations.relation_type_second_snap)
        if not(self.relations.relation_type_third_snap == ""):
            dico_snap.append(self.relations.relation_type_third_snap)
        if not(self.relations.relation_type_fourth_snap == ""):
            dico_snap.append(self.relations.relation_type_fourth_snap)
        dico_snap.append(self.relations.relation_type_code)
        return dico_snap


##############################################################################################################
#                                            AUTHORSHIP_LINK                                                 #
##############################################################################################################

class Authorship_link(db.Model):
    __tablename__ = "authorship_link"
    authorship_link_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_link_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_link_link_id = db.Column(db.Integer, db.ForeignKey('link.link_id'))
    authorship_link_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# Jointure
    user_link = db.relationship("User", back_populates="author_link")
    link_link = db.relationship("Link", back_populates="authorships_l")

    @staticmethod
    def authorship_l(updated):
        """
        crée l'inscription d'un événement (creation ou modification) concernant un objet de la table Link.
        :param creation : identifiant numérique du lien concerné par l'événement
        """
        entry = Authorship_link(
            authorship_link_user_id=current_user.get_id(),
            authorship_link_link_id=updated.link_id
            )

        try:
            db.session.add(entry)
            db.session.commit()
            return True

        except Exception as why:
            print(why)
            return False

    @staticmethod
    def delete_logs(id_link):
        """ supprime tous les logs concernant un lien à supprimer
        :param id_link : identifiant numérique du lien à supprimer
        """
        logs = Authorship_link.query.filter(Authorship_link.authorship_link_link_id == id_link).all()
        for log in logs:
            db.session.delete(log)
            db.session.commit()

##############################################################################################################
#                                            AUTHORSHIP_PERSON                                               #
##############################################################################################################

class Authorship_person(db.Model):
    __tablename__ = "authorship_person"
    authorship_person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    authorship_person_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    authorship_person_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_person_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
# Jointure
    person = db.relationship("Person", back_populates="authorships_p")
    user_person = db.relationship("User", back_populates="author_person")

    @staticmethod
    def authorship(updated):
        """
        crée l'inscription d'un événement (creation ou modification) concernant un objet de la table Person.
        :param creation : identifiant numérique de la notice concernée par l'événement
        """
        entry = Authorship_person(
            authorship_person_user_id=current_user.get_id(),
            authorship_person_person_id=updated.person_id
            )

        try:
            db.session.add(entry)
            db.session.commit()
            return True

        except Exception as why:
            print(why)
            return False


    @staticmethod
    def delete_logs(id_person):
        """ supprime tous les logs concernant une personne à supprimer
        :param id_link : identifiant numérique de la personne à supprimer
        """
        logs = Authorship_person.query.filter(Authorship_person.authorship_person_person_id == id_person).all()
        for log in logs:
            db.session.delete(log)
            db.session.commit()
