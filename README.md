# Application de gestion d'un dictionnaire prosopographique 
Ce repository contient l'ensemble des éléments nécessaires à l'installation d'une application Flask dédiée à un dictionnaire proposographique. Cette application est développée dans le cadre du cours Python du Master 2 Technologies numériques appliquées à l'histoire de l'Ecole nationale des chartes, selon les consignes suivantes :    

## Consignes 
> En groupe de 5 personnes maximum, vous choisirez un sujet au choix parmi la liste proposée. Des limitations différentes peuvent être indiquées pour certains projets. Rendu le 15 Avril.  
>  
> **Consignes globales**  
> - Les rendus se feront via git et github en particulier sur des dépôts de https://github.com/Chartes-TNAH.
> - La notation peut différer d'un membre à l'autre du groupe.
> - Une documentation pour la mise en place du projet (installation) sera mise à disposition. Le README de ce dépôt peut être utilisé comme référence.
> - Des données de tests seront fournies afin d'utiliser l'application.
> - (Optionnel) Des tests unitaires seront fournis Note: cet encart dépendra de l'évolution du cours.
> - Le design final ne sera pas évalué bien qu'il soit recommandé que l'ensemble reste lisible et utilisable.
>   
> **Application de gestion d'un dictionnaire prosopographique**
> Dans le cadre de l'établissement d'un projet de dictionnaire de personnes et de liens entre celles-ci, vous développerez une application respectant les besoins suivants :  
> - On s'inspirera pour les champs de pages telles que https://www.wikidata.org/wiki/Q5648  
> - Les champs seront réfléchis à partir de champs d'ontologies RDF (FOAF par exemple)  
> - On pourra chercher à l'intérieur de la base  
> - Un système de compte sera utilisé (avec validation des comptes)  
> - On pourra lier des personnes entre elles  
> - Ces relations seront qualifiées à partir de la l'ontologie SNAP ( http://snap.dighum.kcl.ac.uk/owl/snap.owl)  
> - On pourra lier les individus à d'autres identifiants  
> - Un affichage en JSON-LD sera possible via une API simple  


Ce document contient l'ensemble des procédures d'installation pour utiliser cette application. 

## Installation 
### OS X / Mac
[...]

### Linux (Ubuntu/Debian)
#### Première utilisation  
Vous aurez sûrement besoin d'installer **python3**, **virtualenv** et **pip**, pour cela, ouvrez un terminal et tapez :  
`sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv`

Lancez le dossier **dico-proso/** dans un terminal et tapez :  
`virtualenv ~/.dicoproso -p python3`  
Cela crée un environnement virtuel dans lequel pourront être installés les packages utilisés. Pour activer cet environnement virtuel, tapez :  
`source ~/.dicoproso/bin/activate`  
*Cette commande sera nécessaire à chaque fois que vous voudrez activer l'environnement virtuel pour utiliser l'application.*  
  
Dans le même terminal, tapez :  
`pip install requirements.txt`  
Cela installe les packages requis pour faire fonctionner l'application.  

Pour lancer l'application, tapez :  
`python3 run.py`  

#### Utilisations ultérieures :
Lancez le terminal depuis le dossier principal et entrez :  
`source ~/.dicoproso/bin/activate`  
puis  
`python3 run.py

## Contributeur.ices 
- Ekaterina Batova
- Alix Chagué
- Eglantine Charmetant
- Léa Duflos
- Aurélia Vasile
