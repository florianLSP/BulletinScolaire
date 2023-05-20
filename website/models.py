from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# class Eleve(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     statut = db.Column(db.String(20))
#     email = db.Column(db.String(150), unique=True)
#     nom = db.Column(db.String(50))
#     prenom = db.Column(db.String(50))
#     mdp = db.Column(db.String(250))
#     notes = db.relationship('Note')

# class Professeur(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     statut = db.Column(db.String(20))
#     email = db.Column(db.String(150), unique=True)
#     nom = db.Column(db.String(50))
#     prenom = db.Column(db.String(50))
#     mdp = db.Column(db.String(250))
#     notes = db.relationship('Note')
    
class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    statut = db.Column(db.Boolean)
    email = db.Column(db.String(150), unique=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    mdp = db.Column(db.String(250))
    notes = db.relationship('Note')
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matiere = db.Column(db.String(50))
    note = db.Column(db.Integer)
    coef = db.Column(db.Integer)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    noteFinal = db.Column(db.Float)
    moyenne = db.Column(db.Float)