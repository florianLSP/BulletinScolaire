from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .models import Eleve, Professeur, Note
from . import db
from .auth import auth

# création d'une intance de blueprint 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home(): 
    return render_template("accueil.html", user=current_user)

@views.route('/eleveAccueil', methods=['GET', 'POST'])
@login_required
def eleveAccueil():
    eleve = Eleve.query.get(current_user.id)
    notes = eleve.notes
    moyenne = calculer_moyenne(eleve.id)
    return render_template("eleveAccueil.html", user=current_user, eleve=eleve, notes=notes, moyenne=moyenne)

@views.route('/profAccueil', methods=['GET', 'POST'])
@login_required
def profAccueil():
    prof = Professeur.query.get(current_user.id)
    return render_template("profAccueil.html", user=current_user, prof=prof)

@views.route('/ajouterNote', methods=['GET', 'POST'])
@login_required
def ajouterNote():
    if request.method == 'POST':
        matiere = request.form.get('matiere')
        note = request.form.get('note')
        coef = request.form.get('coef')
        eleve_email = request.form.get('eleve')
        
        print(matiere)
        print(type(matiere))
        print(note)
        print(type(note))
        print(coef)
        print(type(coef))
        print(eleve_email)
        print(type(eleve_email))
        
        user = Eleve.query.filter_by(email=eleve_email).first()


        if user:
            if int(coef) == 10:
                if int(note) > 10:
                    flash('La note ne peut pas être supérieur à 10', category='error')
                elif int(note) < 0:
                    flash('La note ne peut pas être inférieur à 0', category='error')
                else:
                    noteFinal = miseSur20(note, coef)
                    moyenne = calculer_moyenne(user.id)
                    print(f'la moyenne est de {moyenne}')
                    print(type(moyenne))
                    print(f'la note finale est : {noteFinal}')
                    print(type(noteFinal))
                    new_note = Note(matiere=matiere, note=note, coef=coef, eleve_id=user.id, noteFinal=noteFinal, moyenne=moyenne)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    return redirect(url_for('views.ajouterNote'))
                
            if int(coef) == 20:
                if int(note) > 20:
                    flash('La note ne peut pas être supérieur à 20', category='error')
                elif int(note) < 0:
                    flash('La note ne peut pas être inférieur à 0', category='error')
                else:
                    noteFinal = float(note)
                    moyenne = calculer_moyenne(user.id)
                    print(f'la moyenne est de {moyenne}')
                    print(type(moyenne))
                    print(f'la note finale est : {noteFinal}')
                    print(type(f'le type de la note finale est : {noteFinal}'))
                    new_note = Note(matiere=matiere, note=note, coef=coef, eleve_id=user.id, noteFinal=noteFinal, moyenne=moyenne)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    return redirect(url_for('views.ajouterNote')) 
        else:
            flash('L\'email ne correspond à aucun élève!')
    return render_template("ajouterNote.html", user=current_user)

@views.route('/parametre', methods=['GET', 'POST'])
@login_required
def parametre():
    # Envoyer les données pour pré remplir le formulaire paramètres
    eleve = current_user
    eleve_id = eleve.id
    email = eleve.email
    prenom = eleve.prenom
    nom = eleve.nom
    mdp = eleve.mdp
    
    if request.method == 'POST':
        # récupération de toute les données du formulaire
        up_email = request.form.get('email')
        up_prenom = request.form.get('prenom')
        up_nom = request.form.get('nom')
        up_mdp = request.form.get('mdp1')
        new_mdp1 = request.form.get('newMDP1')
        new_mdp2 = request.form.get('newMDP2')
        
        if mdp == up_mdp:
            if email != up_email:
                eleve.email = up_email
                check_email = eleve.email
                print(check_email)
                flash('Succès lors de la modification de l\'email!', category='success')
            else: 
                eleve.email = email

            if prenom != up_prenom:
                eleve.prenom = up_prenom
                check_prenom = eleve.prenom
                print(check_prenom)
                flash('Succès lors de la modification du prénom!', category='success')
            else:
                eleve.prenom = prenom
                    
            if nom != up_nom:
                eleve.nom = up_nom
                check_nom = eleve.nom
                print(check_nom)
                flash('Succès lors de la modification du nom!', category='success')
            else:
                eleve.nom = nom
                    
            if mdp != new_mdp1:
                if new_mdp1 == new_mdp2:
                    eleve.mdp = new_mdp1
                    check_mdp = eleve.mdp
                    print(check_mdp)
                    flash('Succès lors de la modification du mot de passe!', category='success')
                else:
                    flash('Les nouveaux mots de passe doivent être identiques!', category='error')
                        
            db.session.commit()
            return redirect(url_for('views.home')) 
        else:
            flash('Le mot de passe est incorrect, aucune modification a été faite!', category='error')
            
    return render_template("parametre.html", user=current_user, email=email, prenom=prenom, nom=nom, mdp=mdp)


def miseSur20(note, coef):
    note_final = float(note)/float(coef)*20 
    return float(note_final)

def calculer_moyenne(eleve_id):
    eleve = Eleve.query.filter_by(id=eleve_id).first()
    notes_finales = Note.query.filter_by(eleve_id=eleve_id).with_entities(Note.noteFinal).all()
    total_notes = sum(note[0] for note in notes_finales)
    nb_notes = len(notes_finales)

    if nb_notes > 0:
        moyenne = total_notes / nb_notes
        return (round(moyenne, 2))
    else:
        return None