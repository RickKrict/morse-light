##########
# IMPORT #
##########
from controllers.controllerConfig import ControllerConfig
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit, QSpinBox, QDoubleSpinBox, QDialog, QRadioButton, QMainWindow

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"


class ConfigMorse(QDialog):
    def __init__(self, fenetrePrincipale):
        """
        initialise la fenetre de configuration

        Parameters
        ----------
        fenetrePrincipale : QMainWindow
            La fenetre principale qui contient un attribut traducteur qui sera modifié.
        """
        # initialisation de la fenetre
        super(ConfigMorse, self).__init__()

        if not isinstance(fenetrePrincipale, QMainWindow):
            raise TypeError("ConfigMorse: fenetrePrincipale doit etre de type QMainWindow.")

        self.fenetrePrincipale = fenetrePrincipale
        self.setWindowTitle("Configuration")
        uic.loadUi('views/config.ui', self)
        #self.setFixedWidth(719)
        #self.setFixedHeight(328)

        self.controller = ControllerConfig(self)

        # récupération des éléments interactifs
        self.portGpio = self.findChildren(QSpinBox, 'portGpio')[0]
        self.tempsPoint = self.findChildren(QDoubleSpinBox, 'tempsPoint')[0]
        self.barreDeStatus = self.findChildren(QLineEdit, 'barreStatus')[0]
        self.barreDeStatus.setReadOnly(True)
        self.fauxVerbose = self.findChildren(QRadioButton, 'fauxVerbose')[0]
        self.fauxVerbose.setChecked(True)
        self.vraiVerbose = self.findChildren(QRadioButton, 'vraiVerbose')[0]

        self.tempsPoint.setSingleStep(0.1)
        self.tempsPoint.setRange(0.1, 10)
        self.portGpio.setRange(1,40)
        self.boutonsSortie.accepted.connect(self.controller.check)

    def show(self):
        self.controller.rafraichissement()
        super(ConfigMorse, self).show()
