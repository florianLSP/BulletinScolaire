from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Eleve(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
    
class Professeur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matiere = db.Column(db.String(50))
    note = db.Column(db.Integer)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'))
    professeur_id = db.Column(db.Integer, db.ForeignKey('professeur.id'))