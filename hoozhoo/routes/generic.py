from flask import render_template, request, flash, redirect
from ..app import app
from ..modeles.donnees import Person, Link, Relation_type
from ..modeles.utilisateurs import User

#variable à utiliser pour la pagination de la page recherche et index
PERSONNES_PAR_PAGES = 3

@app.route("/")
def accueil():
    """ Route permettant l'affichage de la page d'accueil
    """

    # récupération des 4 dernières notices créées pour affichage
    personnes = Person.query.order_by(Person.person_id.desc()).limit(4).all()
    print (type(personnes))

    return render_template("pages/accueil.html", personnes=personnes)


@app.route("/a-propos")
def about():
    return render_template("pages/about.html")

@app.route("/index")
def index():
    """
    Route qui affiche la liste des personnes (Nom, prenom) de la base.
    """
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    titre="Index"
#creation de la pagination avec la methode .paginate qui remplace le .all dans la requête sur la base
    personnes = Person.query.order_by(Person.person_name).paginate(page=page, per_page= PERSONNES_PAR_PAGES)
    return render_template("pages/index.html", personnes=personnes, titre=titre)



@app.route("/person/<int:identifier>")
def notice(identifier):
    """
    Route qui affiche la notice descriptive de la personne
    :param identifier: identifiant numérique de la personne
    """
    personneUnique = Person.query.get(identifier)

    listLien = personneUnique.link_pers1

    return render_template("pages/notice.html", unique=personneUnique, listLien=listLien)

@app.route("/creer-lien", methods=["GET", "POST"])
def creer_lien():
    """
    route permettant à un utilisateur enregistré de créer un ou plusieurs liens entre des personnes existant dans la base
    """
    listRelation = Relation_type.query.all()

    if request.method == "POST":
        status, data = Link.create_link(
        link_person1=request.form.getlist("link_1_person[]", None),
        link_relation_type=request.form.getlist("link_relation_type[]", None),
        link_person2=request.form.getlist("link_2_person[]", None)
        )

        if status is True:
            flash("Création de lien(s) réussie !", "success")
            return redirect("/creer-lien")

        else:
            flash("La création de lien(s) a échoué pour les raisons suivantes : " + ",".join(data), "danger")
            return render_template("pages/creer_lien.html", listRelation=listRelation)
    else:
        return render_template("pages/creer_lien.html", listRelation=listRelation)


@app.route("/modification/<int:identifier>", methods=["POST", "GET"])
#@login_required #désactivé pour le test
def modification (identifier):
    """
    route permettant de modifier un formulaire avec les données d'une personne
    :param identifier: identifiant numérique de la personne récupéré depuis la page notice
    """
    # renvoyer sur la page html les éléments de l'objet personne correspondant à l'identifiant de la route
    if request.method == "GET":
        personne_origine = Person.query.get(identifier)
        return render_template("pages/modification_personne.html", personne_origine=personne_origine)

        # on récupère les données du formulaire modifié
    else:
        status, personneModifier= Person.modifier_person(
            id = identifier,
            nom = request.form.get("nom", None),
            prenom = request.form.get("prenom", None),
            surnom = request.form.get("surnom", None),
            description = request.form.get("description", None),
            date_naissance = request.form.get("date_naissance", None),
            date_deces = request.form.get("date_deces", None),
            genre = request.form.get("genre", None),
            id_externes = request.form.get("id_externes", None),
            fonctions = request.form.get ("fonctions_occupations", None),
            langues = request.form.get ("langues", None),
            nationalite = request.form.get ("pays_nationalite", None),
            nom_naissance = request.form.get ("nom_languematernelle", None)

        )

        if status is True:
            flash("Modification réussie !", "success")
            return render_template ("pages/notice.html", unique=personneModifier, listLien=personneModifier.link_pers1)
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(personneModifier), "danger")
            personne_origine = Person.query.get(identifier)
            return render_template("pages/modification_personne.html", personne_origine=personne_origine)



@app.route("/creer-personne", methods=["GET", "POST"])
#@login_required #désactivation pour test
def creer_personne():
    """ route permettant à l'utilisateur de créer une notice personne """
    personne = Person.query.all()
    if request.method == "POST":
        # méthode statique create_person() à créer sous Person
        status, data = Person.create_person(
        nom=request.form.get("nom", None), 
        prenom=request.form.get("prenom", None),
        surnom=request.form.get("surnom", None),
        nom_languematernelle=request.form.get("nom_languematernelle", None),
        date_naissance=request.form.get("date_naissance", None),
        date_deces=request.form.get("date_deces", None),
        pays_nationalite=request.form.get("pays_nationalite", None),
        langues=request.form.get("langues", None),
        genre=request.form.get("genre", None),
        fonctions_occupations=request.form.get("fonctions_occupations", None),
        description=request.form.get("description", None),
        id_externes=request.form.get("id_externes", None)
        )
        

        if status is True:
            flash("Création d'une nouvelle personne réussie !", "success")
            return redirect("/creer-personne")
        else:
            flash("La création d'une nouvelle personne a échoué pour les raisons suivantes : " + ", ".join(data), "danger")
            return render_template("pages/creer_personne.html")

    else:
        return render_template("pages/creer_personne.html")



@app.route("/contact")
def contact():
    return render_template("pages/contact.html")


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
            motdepasse_confirmation=request.form.get("motdepasse_confirmation", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/modifierlien/<int:identifier>", methods=["GET", "POST"])
def modification_lien(identifier):
    """
    Route qui affiche un lien existant dans la base pour l'éditer
    :param identifier: identifiant numérique du lien
    """
    listRelation = Relation_type.query.all()
    lienUnique = Link.query.get(identifier)

    if request.method == "GET":
        return render_template("pages/modification_lien.html", unique=lienUnique, listRelation=listRelation)

    # sinon en méthode POST : 
    else: 
        personneOrigine = request.form.get("link_1_person", None)
        
        status, data = Link.modifier_link(
            id = identifier,
            link_person1_id = personneOrigine,
            link_relation_type = request.form.get("link_relation_type", None),
            link_person2_id = request.form.get("link_2_person", None)
            )

        if status is True :
            flash("Modification réussie !", "success")
            return redirect("/person/" + str(personneOrigine) )

        else:
            flash("Les erreurs suivantes empêchent l'édition du lien : " + ",".join(data), "danger")
            return render_template("pages/modification_lien.html", unique=lienUnique, listRelation=listRelation)





@app.route("/confirmer-supprimer/<int:identifier>", methods=["GET", "POST"])
def suppression_lien(identifier):
    """
    Route qui affiche les informations du lien à supprimer et qui demande confirmation
    :param identifier : identifiant numérique du lien
    """
    listRelation = Relation_type.query.all()
    lienUnique = Link.query.get(identifier)

    if request.method == "GET":
        return render_template("pages/suppr_lien.html", unique=lienUnique, listRelation=listRelation)

    else:

        status = Link.delete_link(link_id=identifier)

        if status is True :
            flash("Lien supprimé !", "success")
            return redirect("/person/" + str(lienUnique.link_person1_id))

        else:
            flash("La suppression a échoué.", "danger")
            return redirect("/person/" + str(lienUnique.link_person1_id))

