##########
# IMPORT #
##########
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QRadioButton, QDialog
from morse import TraducteurMorse as morse
import logging

# TODO lier le mode verbose
# TODO changer le QLineEdit par une zone de texte

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"

class ControllerConfig:
    def __init__(self, fenetreConfig):
        """
        initialise le controller

        Parameters
        ---------
        fenetreConfig : QDialog
            Fenetre liée au controller
        """
        if not isinstance(fenetreConfig, QDialog):
            raise TypeError("ControllerConfig: fenetreConfig doit etre de type QDialog.")
        self.fenetreConfig = fenetreConfig
        self.fenetrePrincipale = fenetreConfig.fenetrePrincipale

    def rafraichissement(self):
        """
        Remets à jour l’interface de configuration.
        """
        self.fenetreConfig.portGpio.setValue(self.fenetrePrincipale.controller.traducteur.portGpio)
        self.fenetreConfig.tempsPoint.setValue(self.fenetrePrincipale.controller.traducteur.point)
        self.fenetreConfig.barreStatus.setText("")
        self.fenetreConfig.barreStatus.setStyleSheet("QLineEdit { background: white }")

    def majMorse(self, point, portGpio):
        """
        Permet de mettre à jour la classe morse avec les valeurs entrées

        Parameters
        ---------
        point : float 
            temps en seconde d’un point

        portGpio : int
            port gpio du raspberry qui sera utilisé 
        """
        try:
            traducteur = morse(portGpio, point)
            self.fenetrePrincipale.controller.traducteur = traducteur
            self.fenetreConfig.accept()
            if self.fenetreConfig.vraiVerbose.isChecked():
                logging.getLogger('morse-light').setLevel(logging.INFO)
            else:
                self.fenetrePrincipale.barreDeStatus.setText("")
                self.fenetrePrincipale.barreDeStatus.setStyleSheet("QLineEdit { background: white }")
                logging.getLogger('morse-light').setLevel(logging.WARNING)
        except Exception as err:
            message = QMessageBox(QMessageBox.Warning, "Erreur", "Une des valeurs entrées n'est pas bonne", QMessageBox.Ok)
            message.exec()
            self.fenetreConfig.barreStatus.setText(str(err))
            self.fenetreConfig.barreStatus.setStyleSheet("QLineEdit { background: #ff5050 }")

    def check(self):
        """
        Vérifie si les valeurs entrées sont correctes, génére une fenetre d’erreur sinon.
        """
        point = self.fenetreConfig.tempsPoint.value()
        portGpio = self.fenetreConfig.portGpio.value()

        if point >= 2:
            message = QMessageBox(QMessageBox.Question, "Attention", "Le temps entré est supérieur à 2 secondes. Souhaitez-vous continuer ?", QMessageBox.Yes | QMessageBox.No)
            res = message.exec_()
            if res == QMessageBox.Yes:
                self.majMorse(point, portGpio)
        else:
            self.majMorse(point, portGpio)
