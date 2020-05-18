############################################
#                                          #
#       script permettant d’utiliser       #
#   facilement le traducteur texte/morse   #
#                                          #  
############################################

##########
# IMPORT #
##########
import argparse
from signal import signal, SIGINT
import logging
try:
    from morse import TraducteurMorse as morse
except:
    exit(1)

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GLP3 or later"

parser = argparse.ArgumentParser(
        description="Permet d’entrer des phrases ou des mots qui seront traduient en morse grace à la classe traducteurMorse. Cette traduction sera ensuite convertie en flash lumineux."
        )
parser.add_argument('-m', '--message', nargs=1, help="Permet de juste passer un message à traduire.")
parser.add_argument('--point', nargs=1, type=float, help="Définit la durée en seconde d’un point.")
parser.add_argument('--gpio', nargs=1, type=int, help="Définit le port GPIO du relai ou de la LED.")
parser.add_argument('-v', '--verbose', action="store_true", help="Affiche de manière détaillée le processus.")
args = parser.parse_args()

if args.verbose:
    logging.getLogger('morse-light').setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

def recupSignal(sig, frame):
    """
    Fonction appelée lorsque l’utilisateur fait Ctrl+C
    Permet de sortir du programme
    """
    print("\nAu revoir !")
    exit(0)

def checkTemps(temps):
    """
    Vérifie si le temps entré n’est pas trop long et est positif

    Parameters
    ----------
    temps : int
        Le temps d’un point en seconde
    """
    if not isinstance(temps, float):
        logging.error("Le temps doit être de type float.")
    elif temps <= 0:
        logging.error("Le temps passé en paramètre est négatif ou égale à zéro")
        exit(1)
    elif temps < 0.1 or temps > 2:
        logging.warning("Le temps passé en paramètre est trop court ou trop long.")
        garderTemps = input("Souhaitez-vous vraiment ce temps ? O/n")
        if garderTemps.lower() != "o":
            print("Annulation...")
            exit(1)

signal(SIGINT, recupSignal)
try:
    if args.point and args.gpio:
        checkTemps(args.point[0])
        traducteur = morse(args.gpio[0], args.point[0])
    elif args.point:
        checkTemps(args.point[0])
        traducteur = morse(point=args.point[0])
    elif args.gpio:
        traducteur = morse(args.gpio[0])
    else:
        traducteur = morse()

    if args.message:
        traducteur.traductionEtEnvoie(args.message[0])
    else:
        print("Entrez ':q' pour quitter le programme.")
        entreUtilisateur = input("Entrez une phrase ou un mot à traduire et à transmettre en morse : ")
        
        while entreUtilisateur != ':q':
            print("\n")
            traducteur.traductionEtEnvoie(entreUtilisateur)
            print("\n")
        
            print("Entrez ':q' pour quitter le programme.")
            entreUtilisateur = input("Entrez une phrase ou un mot à traduire et à transmettre en morse : ")
        print("\nAu revoir !")
except Exception as err:
    logging.error("Une erreur de type %s a été rencontrée. Utilisez l'option -v pour pouvoir voir le message d'erreur.", type(err).__name__)
    logging.info(err)
