from website import create_app

# On appele la fonction qui se trouve dans __init__, on stock la fonction dans une variable qui porte le meme nom que l'app
app = create_app()

# On vérifie que le fichier main.py est le programme principal
if __name__ == '__main__':
    # Si c'est le cas on run l'application en mode debug (ça veut dire que l'app va se recharger automatiquement)
    # et quelle affichera les erreurs.
    app.run(debug = True)