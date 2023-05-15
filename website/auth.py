from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Eleve, Professeur
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email =request.form.get('email')
        prenom =request.form.get('prenom')
        nom =request.form.get('nom')
        mdp1 =request.form.get('mdp1')
        mdp2 =request.form.get('mdp2')

        user_eleve = Eleve.query.filter_by(email=email).first()
        
        if user_eleve:
            print("adresse email deja attribuée")
        elif len(email) < 6:
            pass
        elif len(prenom) < 3:
            pass
        elif len(nom) < 3:
            pass
        elif len(mdp1) <2:
            pass
        elif mdp1 != mdp2:
            pass
        else:
            new_eleve = Eleve(email=email, prenom=prenom, nom=nom, mdp=mdp1)
            db.session.add(new_eleve)
            db.session.commit()
            print(new_eleve)
            

            return render_template("home.html")
    
    return render_template("inscription.html")

@auth.route('/connexion')
def connexion():
    return render_template("connecter.html")

