from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Instanciation de la classe SQLAlchemy et création du nom de la base de données.
db = SQLAlchemy()
DB_NAME = "database.db"

# Création de la fonction "create_app" qui permet de créer l'application web flask.
def create_app():
    # cette ligne permet de créer l'app en lui donnant le nom "__name__"
    app = Flask(__name__)
    # Configuration d'une clé secrete qui permet de protéger les cookies et les sessions contre la falsification de requête
    app.config['SECRET KEY'] = 'la clé secrete'
    # Configuration de l'emplacement de la bd pour l'app. Dans ce cas il s'agit d'une bd sqlite situé dans le répertoire que l'application.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialisation de la base de données
    db.init_app(app)
    
    # Importation du blueprint views
    from .views import views
    from .auth import auth
    # Enregistre dans app le blueprint views. Flas redirigera vers cette vue quand cet url sera rentrée.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Eleve, Professeur, Note
    with app.app_context():
        db.create_all()

         
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('La base données est créée')