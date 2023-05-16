from flask import Blueprint, request, render_template, flash
from flask_login import login_required, current_user
from .models import Eleve, Professeur, Note
from . import db

# création d'une intance de blueprint 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():        
    return render_template("home.html", eleve=current_user)

@views.route('/ajouterNote')
def ajouterNote():
    return render_template("ajouterNote.html")

@views.route('/parametre')
def parametre():
    return render_template("parametre.html")