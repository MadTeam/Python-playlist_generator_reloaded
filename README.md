Python-playlist_generator_reloaded
==================================

Usage :
main.py nom {xspf,m3u,pls} temps [OPTIONS]

Description :
Ce générateur de playlist permet de générer un fichier dans un format spécial qui contient un ensemble de titres musicaux selon les choix de l'utilisateur.

Voici l'utilisation basique du programme (sans options avancées), l'ensemble des options listées sont obligatoire pour générer la playlist.
- (commande de base) il s'agit du nom du fichier qui sera exécuté pour utiliser le programme (".\textbackslash{}main.py")
- (nom) nom du fichier de sortie (inutile de préciser l'extension, elle sera ajouter automatiquement selon l'option suivante)
- (format) ajoute l'extension au fichier selon 3 choix possible (xspf, m3u ou pls)
- (temps) permet de spécifier la durée totale de la playlist en minute
- ('-h' '--help' '--aide') affiche l'aide
- ('-v' '--verbeux') permet l'affichage détaillé des opérations (ces informations sont également disponible dans le fichier de log)

note : le mode verbeux n'affiche pas grand chose s'il est envoyé seul.


Pré-requis
- python3
- python-pycogs
- python3-sqlalchemy
