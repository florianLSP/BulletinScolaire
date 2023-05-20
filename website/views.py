from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .models import Utilisateur, Note
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
    eleve = Utilisateur.query.get(current_user.id)
    notes = eleve.notes
    moyenne = calculer_moyenne(int(eleve.id))
    return render_template("eleveAccueil.html", user=current_user, eleve=eleve, notes=notes, moyenne=moyenne)

# @views.route('/profAccueil', methods=['GET', 'POST'])
# @login_required
# def profAccueil():
#     professeur = Utilisateur.query.get(current_user.id)
#     return render_template("profAccueil.html", user=current_user, professeur=professeur)

@views.route('/profAccueil', methods=['GET', 'POST'])
@login_required
def profAccueil():
    professeur = Utilisateur.query.get(current_user.id)
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
        
        user = Utilisateur.query.filter_by(email=eleve_email).first()


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
                    new_note = Note(matiere=matiere, note=note, coef=coef, utilisateur_id=user.id, noteFinal=noteFinal, moyenne=moyenne)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    # return redirect(url_for('views.profAccueil'))
                    return render_template("profAccueil.html", user=current_user)
                
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
                    new_note = Note(matiere=matiere, note=note, coef=coef, utilisateur_id=user.id, noteFinal=noteFinal, moyenne=moyenne)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    # return redirect(url_for('views.ajouterNote')) 
                    return render_template("profAccueil.html", user=current_user)
        else:
            flash('L\'email ne correspond à aucun élève!')
    return render_template("profAccueil.html", user=current_user, professeur=professeur)

@views.route('/parametre', methods=['GET', 'POST'])
@login_required
def parametre():
    # Afficher les données de l'utilisateur dans le formulaire.
    email = current_user.email
    prenom = current_user.prenom
    nom = current_user.nom
    mdp = current_user.mdp
    
    # Récupérer les données du formulaire.
    if request.method == 'POST':
 
        email_form = request.form.get('email')
        prenom_form = request.form.get('prenom')
        nom_form = request.form.get('nom')
        mdp_form = request.form.get('mdp1')
        mdp1_new_form = request.form.get('newMDP1')
        mdp2_new_form = request.form.get('newMDP2')
        
        if mdp_form == mdp:
            if email_form != email:
                current_user.email = email_form
                db.session.commit()
                flash('Succès lors de la modification de l\'email!', category='success')
                
            if prenom_form != prenom:
                current_user.prenom = prenom_form
                db.session.commit()
                flash('Succès lors de la modification du prénom', category='success')
                
            if nom_form != nom:
                current_user.nom = nom_form
                db.session.commit()
                flash('Succès lors de la modification du nom', category='success')
            
            if mdp1_new_form == "" or mdp2_new_form=="":
                current_user.mdp = mdp  
            elif mdp1_new_form == mdp2_new_form:
                current_user.mdp = mdp1_new_form
                db.session.commit()
                flash('Succès lors de la modification du nom', category='success')
            else:
                flash('Les nouveaux mdp doivent être identiques', category='error')
        else: 
            flash('Le mot de passe n\'est pas correct', category='error')     
            
    else : 
        email_afficher = current_user.email
        prenom_afficher= current_user.prenom
        nom_afficher= current_user.nom
          

    # Mettre à jour les données qui ont changé.
    return render_template("parametre.html", user=current_user, email=email, prenom=prenom, nom=nom)


def miseSur20(note, coef):
    note_final = float(note)/float(coef)*20 
    return float(note_final)

def calculer_moyenne(eleve_id):
    eleve = Utilisateur.query.filter_by(id=eleve_id).first()
    notes_finales = Note.query.filter_by(utilisateur_id=eleve_id).with_entities(Note.noteFinal).all()
    total_notes = sum(note[0] for note in notes_finales)
    nb_notes = len(notes_finales)

    if nb_notes > 0:
        moyenne = total_notes / nb_notes
        return (round(moyenne, 2))
    else:
        return None