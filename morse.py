##################################
#                                #
#   prototype de convertisseur   #
#     texte -> morse avec la     #
#           lumière              #
#                                #
##################################

##########
# IMPORT #
##########
from time import sleep
import unicodedata
import logging 
try:
    import RPi.GPIO as GPIO
except ImportError:
    logging.error("Dépendance RPi introuvable.")
    raise
except RuntimeError:
    logging.error("Lancez ce programme sur un Raspberry.")
    raise

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"

class TraducteurMorse:
    def __init__(self, portGpio=7, point=0.1):
        """
        Initialise la durée d'un point et le port GPIO de la led ou du relai.

        Parameters
        ----------
        portGpio : int
            Port GPIO qui sera utilisé. 7 par défaut.
        point : float
            Temps en seconde de la durée d'un point. 0.1 par défaut.
        
        Raises:
        -------
        TypeError
            Si les paramètes entrés ne sont pas du bon type.

        ValueError
            Si le port GPIO est incorrect ou si le temps est négatif ou nul.
        """
        global loggerMorse
        loggerMorse = logging.getLogger("morse-light")
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)

        if not isinstance(portGpio, int):
            loggerMorse.error("Le port GPIO doit être de type int.")
            raise TypeError("Le port GPIO doit être de type int.")

        if not isinstance(point, float):
            loggerMorse.error("Le temps d'un point doit être de type float.")
            raise TypeError("Le temps d'un point doit être de type float.")

        self.point = point 
        if point <= 0:
            loggerMorse.error("Durée négative ou nulle.")
            raise ValueError("Durée négative ou nulle.")
        if point > 2:
            loggerMorse.warning("Durée du point supérieur à 2 secondes.")

        # Configuration du port GPIO
        self.portGpio = portGpio
        try :
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.portGpio, GPIO.OUT)
        except ValueError:
            loggerMorse.error("Le port GPIO entré n’existe pas.")
            raise

        self.CODE_MORSE = {
            'a':"._",
            'b':"_...",
            'c':"_._.",
            'd':"_..",
            'e':".",
            'f':".._.",
            'g':"__.",
            'h':"....",
            'i':"..",
            'j':".___",
            'k':"_._",
            'l':"._..",
            'm':"__",
            'n':"_.",
            'o':"___",
            'p':".__.",
            'q':"__._",
            'r':"._.",
            's':"...",
            't':"_",
            'u':".._",
            'v':"..._",
            'w':".__",
            'x':"_.._",
            'y':"_.__",
            'z':"__..",
            '1':".____",
            '2':"..___",
            '3':"...__",
            '4':"...._",
            '5':".....",
            '6':"_....",
            '7':"__...",
            '8':"___..",
            '9':"____.",
            '0':"_____",
            " ":" "
        }
    
    def codageMorse(self, mot):
        """
        Fonction traduisant un mot en morse
        
        Parameters
        ----------
        mot : str
            Le mot à traduire en morse
        
        Returns
        -------
        array of str
            Un tableau contenant les symboles. Exemple : ["_","."]

        Raises
        ------
        TypeError
            Si le paramètre mot n'est pas de type str.
        """
        if not isinstance(mot, str):
            loggerMorse.error("codageMorse() : le mot passé en paramètre n’est pas de type str.")
            raise TypeError("mot doit être de type str.")

        mot = unicodedata.normalize('NFKD', mot).encode('ascii', 'ignore')
        mot = mot.decode()
        loggerMorse.info("Traduction du mot %s", mot)
        motMorse = []
        for lettre in mot:
            symbole = self.CODE_MORSE.get(lettre, " ") 
            loggerMorse.info("%s -> %s", lettre, symbole)
            motMorse.append(symbole)

        return motMorse

    def decodageMorse(self, motMorse):
        """
        Décode le mot en morse en texte

        Parameters
        -----------
        motMorse : list
            Mot qui va etre décodé. Doit etre au format : ['._', '.'] par ex

        Returns
        --------
        str
            Le mot traduit

        Raises
        ------
        TypeError
            Si le paramètre mot n’est pas du type str
        """
        if not isinstance(mot, list):
            loggerMorse.error("codageMorse() : le mot passé en paramètre n’est pas de type list.")
            raise TypeError("mot doit être de type list.")

        loggerMorse.info("Traduction du mot %s", motMorse)
        mot = ""
        listeClefs = list(self.CODE_MORSE.keys())
        listeValeurs = list(self.CODE_MORSE.values())
        for symbole in motMorse:
            try:
                lettre = listeClefs[listeValeurs.index(symbole)]
                loggerMorse.info("%s -> %s", symbole, lettre)
                mot += lettre
            except ValueError:
                loggerMorse.warning("Symbole inconnu : %s. Remplacement par un espace.", symbole)
                mot += "-"

        return mot

    def lumiere(self, symbole):
        """
        Allume la LED selon le symbole passé en paramètre

        Parameters
        ----------
        symbole : str
            Le symbole qui va déterminer la durée d'allumage de la lampe.
            Doit être _ ou .
        """
        if symbole == "_":
            loggerMorse.info("Allumage. Durée : 3 points.")
            GPIO.output(self.portGpio, GPIO.HIGH)
            sleep(3 * self.point)
        elif symbole == ".":
            loggerMorse.info("Allumage. Durée : 1 points.")
            GPIO.output(self.portGpio, GPIO.HIGH)
            sleep(self.point)
        else:
            loggerMorse.warning("Caractère inconnu :", symbole)
    
    def eteint(self, temps=1):
        """
        Eteint la LED selon le temps passé en paramètre.

        Parameters
        ----------
        temps : int
            Le temps d'extinction en points. Exemple, temps = 7 alors la lampe s'éteint 7 * durée d'un poitn.
            Valeur par défaut : 1

        Raises
        ------
        TypeError
            Si le paramètre n'est pas de type int.
        """
        if not isinstance(temps, int):
            loggerMorse.error("eteint() : le temps passé en paramètre n’est pas de type int.")
            raise TypeError("temps doit être de type int.")

        loggerMorse.info("Extinction. Durée : %s points", temps)
        GPIO.output(self.portGpio, GPIO.LOW)
        sleep(temps * self.point)
    
    def envoieMot(self, motMorse, mot=None):
        """
        Transforme un tableau contenant du morse en signaux lumineux.

        Parameters:
        -----------
        motMorse : array of str
            Tableau contenant les symboles morses. 

        mot : str
            Mot qui sera envoyé
        
        Raises
        ------
        TypeError
            Si le paramètre motMorse n'est pas de type list.

        See also:
        --------
        codageMorse : Code un mot en morse.
        """
        if not isinstance(motMorse, list):
            loggerMorse.error("envoieMot() : le mot en morse passé en paramètre n’est pas de type list.")
            raise TypeError("motMorse doit être de type list.")

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.portGpio, GPIO.OUT)

        if mot != None:
            print("=== Envoie du mot :", mot, "===")
        else:
            print("=== Envoie d'un mot ===")
        
        for i in range(len(motMorse)):
            if motMorse[i] is not " ":
                for j, symbole in enumerate(motMorse[i]):
                    self.lumiere(symbole)
                    if j != len(motMorse[i])-1 :
                        self.eteint()
        
                if i < len(motMorse) - 1:
                    if motMorse[i+1] is " ":
                        self.eteint(self.portGpio)
                    else:
                        self.eteint(3)

        loggerMorse.info("Fin de l’envoi du signal.")
        GPIO.output(self.portGpio, GPIO.LOW)
        GPIO.cleanup()

    def traductionEtEnvoie(self, mot):
        """
        Traduit un mot passé en paramètre en morse puis envoie les signaux lumineux.

        Parameters:
        -----------
        mot : str
            Le mot qui serai traduit en morse et converti en signaux lumineux
        """
        motMorse = self.codageMorse(mot)
        self.envoieMot(motMorse, mot)

#test = traducteurMorse(point=0.1)
#test.point = -1
#test.traductionEtEnvoie("test morse &")
