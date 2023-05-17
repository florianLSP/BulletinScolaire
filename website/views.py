from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .models import Eleve, Professeur, Note
from . import db

# création d'une intance de blueprint 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    #TODO
    eleve = current_user
    notes = eleve.notes
    return render_template("home.html", user=current_user, eleve=eleve, notes=notes)

@views.route('/ajouterNote', methods=['GET', 'POST'])
@login_required
def ajouterNote():
    if request.method == 'POST':
        matiere = request.form.get('matiere')
        note = request.form.get('note')
        coef = request.form.get('coef')
        eleve = request.form.get('eleve')
        
        print(matiere)
        print(type(matiere))
        print(note)
        print(type(note))
        print(coef)
        print(type(coef))
        print(eleve)
        print(type(eleve))
        
        user = Eleve.query.filter_by(email=eleve).first()
        print(user)
        
        if user:
            if int(coef) == 10:
                if int(note) > 10:
                    flash('La note ne peut pas être supérieur à 10', category='error')
                elif int(note) < 0:
                    flash('La note ne peut pas être inférieur à 0', category='error')
                else:
                    new_note = Note(matiere=matiere, note=note, coef=coef, eleve_id=user.id)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    return redirect(url_for('views.home'))
                
            if int(coef) == 20:
                if int(note) > 20:
                    flash('La note ne peut pas être supérieur à 20', category='error')
                elif int(note) < 0:
                    flash('La note ne peut pas être inférieur à 0', category='error')
                else:
                    new_note = Note(matiere=matiere, note=note, coef=coef, eleve_id=user.id)
                    db.session.add(new_note)
                    db.session.commit()
                    print(new_note)
                    return redirect(url_for('views.home')) 
        else:
            flash('L\'email ne correspond à aucun élève!')
    return render_template("ajouterNote.html", user=current_user)

@views.route('/parametre')
def parametre():
    return render_template("parametre.html", user=current_user)