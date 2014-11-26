Python-playlist_generator_reloaded
==================================

Usage :
main.py nom {xspf,m3u,pls} temps [OPTIONS]

Description :
Ce générateur de playlist permet de générer un fichier dans un format spécial qui contient un ensemble de titres musicaux selon les choix de l'utilisateur.

Voici l'utilisation basique du programme (sans options avancées), l'ensemble des options listées sont obligatoire pour générer la playlist.
- (commande de base) il s'agit du nom du fichier qui sera exécuté pour utiliser le programme (".\main.py")
- (nom) nom du fichier de sortie (inutile de préciser l'extension, elle sera ajouter automatiquement selon l'option suivante)
- (format) ajoute l'extension au fichier selon 3 choix possible (xspf, m3u ou pls)
- (temps) permet de spécifier la durée totale de la playlist en minute
- ('-h' '--help' '--aide') affiche l'aide
- ('-v' '--verbeux') permet l'affichage détaillé des opérations (ces informations sont également disponible dans le fichier de log)

Il est possible de personnaliser la playlist en choissisant des options (ex : genre musical, artiste, etc).
Ces options sont cumulables tant qu'une même option ne dépasse pas les 100%, ces options prennent par défaut l'union des musiques trouvées.

- {-G \Bar --genre}{ description pourcentage} le genre de la musique
- {-g \Bar --sousgenre}{ description pourcentage} le sous-genre de la musique
- {-a \Bar --artiste}{ description pourcentage} l'artiste de la musique
- {-A \Bar --album}{ description pourcentage} l'album de la musique
- {-t \Bar --titre}{ description pourcentage} le titre de la musique

Pré-requis
- python3
- python-pycogs
- python3-sqlalchemy
