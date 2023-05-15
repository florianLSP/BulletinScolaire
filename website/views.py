from flask import Blueprint, render_template

# création d'une intance de blueprint 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/ajouterNote')
def ajouterNote():
    return render_template("ajouterNote.html")

@views.route('/parametre')
def parametre():
    return render_template("parametre.html")

@views.route('/deconnecter')
def deconnecter():
    return render_template("home.html")