##########
# IMPORT #
##########
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from morse import TraducteurMorse as morse
from utils.morseHandler import MorseHandler
import logging

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"

class ControllerMorse(QRunnable):
    def __init__(self, fenetrePrincipale, traducteur=None):
        """
        Initialise le controller

        Parameters:
        ----------
        fenetrePrincipale : QMainWindow
            fenetre qui utilise le controller

        traducteur : TraducteurMorse
            classe morse qui sera utilisée pour l’envoie de message
        """
        super(ControllerMorse, self).__init__()
        if not isinstance(fenetrePrincipale, QMainWindow):
            raise TypeError("ControllerMorse: fenetrePrincipale doit etre de type QMainWindow.")

        self.fenetrePrincipale = fenetrePrincipale
        logHandler = MorseHandler(self.fenetrePrincipale.barreDeStatus)

        try:
            if traducteur is not None and isinstance(traducteur, morse):
                logging.warning("ControllerMorse: traducteur n’est pas de type TraducteurMorse.")
                self.traducteur = traducteur
            else:
                self.traducteur = morse()
            logging.getLogger('morse-light').setLevel(logging.WARNING)
            logging.getLogger('morse-light').addHandler(logHandler)
        except Exception as err:
            self.fenetrePrincipale.creerErreur(str(err))

    @pyqtSlot()
    def run(self):
        mot = self.fenetrePrincipale.texteMorse.toPlainText()
        try:
            self.fenetrePrincipale.envoyer.setEnabled(False)
            self.fenetrePrincipale.configuration.setEnabled(False)
            self.traducteur.traductionEtEnvoie(mot)
            self.fenetrePrincipale.envoyer.setEnabled(True)
            self.fenetrePrincipale.configuration.setEnabled(True)
        except Exception as err:
            self.fenetrePrincipale.creerErreur(str(err))
        finally:
            self.fenetrePrincipale.controller = ControllerMorse(self.fenetrePrincipale, self.traducteur)
