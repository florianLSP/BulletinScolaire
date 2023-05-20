from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Utilisateur, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    
    if request.method == 'POST':
        
        # je récupère toutes les données du formulaire :
        email = request.form.get('email')
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        mdp1 = request.form.get('mdp1')
        mdp2 = request.form.get('mdp2')
        statut = request.form.get('statut')
        
        #vérification de ce que j'ai récupéré : 
        print(email)
        print(prenom)
        print(nom)
        print(mdp1)
        print(mdp2)
        print(statut)
            
        # en fonction du statut redirection : 
        if statut == 'False' :
            est_eleve = False
            user = Utilisateur.query.filter_by(email=email).first()
            if user:
                flash('Un compte est déjà attribué à cette adresse email.', category='error')
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
            else :
                new_user = Utilisateur(email=email, prenom=prenom, nom=nom, mdp=mdp1, statut=est_eleve)
                db.session.add(new_user)
                db.session.commit()
                print(f'{new_user}, email : {email}, prenom : {prenom}, nom : {nom}, mdp : {mdp1}, statut : {statut}')
                login_user(new_user, remember=True)
                print('super l\'utilisateur à bien été ajouté.')
                flash(f'Bienvenue {prenom} {nom}, votre compte est 100% fonctionnel!', category='success')
                return redirect(url_for('views.eleveAccueil'))
        
        elif statut == 'True':
            est_professeur = True
            user = Utilisateur.query.filter_by(email=email).first()
            if user:
                flash('Un compte est déjà attribué à cette adresse email.')
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
            else :
                new_user = Utilisateur(email=email, prenom=prenom, nom=nom, mdp=mdp1, statut=est_professeur)
                db.session.add(new_user)
                db.session.commit()
                print(f'{new_user}, email : {email}, prenom : {prenom}, nom : {nom}, mdp : {mdp1}, statut : {statut}')
                login_user(new_user, remember=True)
                print('super l\'utilisateur à bien été ajouté.')
                flash(f'Bienvenue {prenom} {nom}, votre compte est 100% fonctionnel!', category='success')
                return redirect(url_for('views.profAccueil'))
            
    return render_template("inscription.html", user=current_user)

@auth.route('/connecter', methods=['GET', 'POST'])
def connexion():
    if request.method=='POST':
        email = request.form.get('email')
        mdp = request.form.get('mdp')
        
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user:
            if user.mdp == mdp:
                flash(f'Succès lors de la connexion! Bonjour {user.prenom} {user.nom}', category='success')
                print(f"Eleve: {user.id}, identifiant : {email}, mdp : {mdp}, statut : {user.statut}")
                
                if user.statut == True:
                    login_user(user, remember=True)
                    return redirect(url_for('views.profAccueil'))
                else:            
                    login_user(user, remember=True)
                    return redirect(url_for('views.eleveAccueil'))
            
    return render_template("connecter.html", user=current_user)

@auth.route('/deconnecter')
@login_required
def deconnecter():
    logout_user()
    print(f"vient de se déco")
    return redirect(url_for('views.home'))


def calculer_moyenne(eleve_id):
    eleve = Utilisateur.query.filter_by(id=eleve_id).first()
    notes_finales = Note.query.filter_by(eleve_id=eleve_id).with_entities(Note.noteFinal).all()
    total_notes = sum(note[0] for note in notes_finales)
    nb_notes = len(notes_finales)

    if nb_notes > 0:
        moyenne = total_notes / nb_notes
        return (round(moyenne, 2))
    else:
        return None