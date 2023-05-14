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
    app.config['SECRET KEY'] = 'clé secrete'
    # Configuration de l'emplacement de la bd pour l'app. Dans ce cas il s'agit d'une bd sqlite situé dans le répertoire que l'application.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialisation de la base de données
    db.init_app(app)