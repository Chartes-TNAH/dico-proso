from warnings import warn

SECRET_KEY = "JE SUIS UN SECRET !"
API_ROUTE = "/api"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)


# Partie tirée de l'exemple 18 de l'application gazetteer, à corriger !
class _TEST:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'mysql://hoozhoo_user:password@localhost/hoozhoo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'mysql://hoozhoo_user:password@localhost/hoozhoo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}
