from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Eleve, Professeur
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        statut = request.form.get('statut')
        email =request.form.get('email')
        prenom =request.form.get('prenom')
        nom =request.form.get('nom')
        mdp1 =request.form.get('mdp1')
        mdp2 =request.form.get('mdp2')
        
        print(statut)
        
        if statut == "eleve":
            user_eleve = Eleve.query.filter_by(email=email).first()
        
            if user_eleve:
                flash('L\'adresse mail est déjà utilisée, veuillez en renseigner une autre.', category='error')
            elif len(email) < 6:
                flash('L\'email doit contenir au moins 6 caractères!', category='error')
            elif len(prenom) < 3:
                flash('Le prénom doit contenir au moins 3 caractères!', category='error')
            elif len(nom) < 3:
                flash('Le nom doit contenir au moins 3 caractères!', category='error')
            elif len(mdp1) < 5:
                flash('Le mot de passe doit au moins 5 caractères!', category='error')
            elif mdp1 != mdp2:
                flash('Les mots de passe ne sont pas identiques!', category='error')
            else:
                new_eleve = Eleve(statut=statut, email=email, prenom=prenom, nom=nom, mdp=mdp1)
                db.session.add(new_eleve)
                db.session.commit()
                login_user(new_eleve, remember=True)
                flash(f'Inscription terminée, bienvenue {prenom}', category='success')
                print(new_eleve)
                return render_template("home.html", user=current_user)
        else:
            user_professeur = Professeur.query.filter_by(email=email).first()
        
            if user_professeur:
                flash('L\'adresse mail est déjà utilisée, veuillez en renseigner une autre.', category='error')
            elif len(email) < 6:
                flash('L\'email doit contenir au moins 6 caractères!', category='error')
            elif len(prenom) < 3:
                flash('Le prénom doit contenir au moins 3 caractères!', category='error')
            elif len(nom) < 3:
                flash('Le nom doit contenir au moins 3 caractères!', category='error')
            elif len(mdp1) < 5:
                flash('Le mot de passe doit au moins 5 caractères!', category='error')
            elif mdp1 != mdp2:
                flash('Les mots de passe ne sont pas identiques!', category='error')
            else:
                user = Professeur(statut=statut, email=email, prenom=prenom, nom=nom, mdp=mdp1)
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flash(f'Inscription terminée, bienvenue {prenom}', category='success')
                print(user)
                return render_template("home.html", user=current_user)
            
    
    return render_template("inscription.html", user=current_user)

@auth.route('/connecter', methods=['GET', 'POST'])
def connexion():
    if request.method=='POST':
        email = request.form.get('email')
        mdp = request.form.get('mdp')
        
        user_eleve = Eleve.query.filter_by(email=email).first()
        user_professeur = Professeur.query.filter_by(email=email).first()

    
        if user_eleve:
            if user_eleve.mdp == mdp:
                user = user_eleve
                flash('Succès lors de la connexion!', category='success')
                print(f"identifiant : {email} et mdp : {mdp}")   
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('La tentative de connexion a échoué!', category='error')
                print('Oups ce n\'est pas bon')
        else: 
            if user_professeur.mdp == mdp:
                user = user_professeur
                flash('Succès lors de la connexion!', category='success')
                print(f"identifiant : {email} et mdp : {mdp}")   
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('La tentative de connexion a échoué!', category='error')
                print('Oups ce n\'est pas bon')
            
    return render_template("connecter.html", user=current_user)

@auth.route('/deconnecter', methods = ['GET', 'POST'])
@login_required
def deconnecter():
    logout_user()
    print("vient de se déco")
    return redirect(url_for('auth.connexion'))