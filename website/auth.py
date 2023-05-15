from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/inscription')
def inscription():
    return render_template("inscription.html")

@auth.route('/connexion')
def connexion():
    return render_template("connecter.html")

