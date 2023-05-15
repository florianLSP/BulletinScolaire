from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Eleve, Professeur
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email = request.form.get('email')
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        mdp1 = request.form.get('mdp1')
        mdp2 = request.form.get('mdp2')
    
    return render_template("inscription.html")

@auth.route('/connexion')
def connexion():
    return render_template("connecter.html")

