##########
# IMPORT #
##########
from sys import exit, argv
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QLineEdit, QApplication, QMessageBox
try:
    from controllers.controllerMorse import ControllerMorse
    from components.config import ConfigMorse as config
    erreur = False
except Exception as err:
    erreur = err

# TODO lier la barre de status aux warnings et aux erreurs ne provoquant pas de crash => barreDeStatus

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"

class InterfaceMorse(QMainWindow):
    def __init__(self):
        super(InterfaceMorse, self).__init__()
        self.threadpool = QThreadPool()

        if erreur:
            self.creerErreur(str(erreur))

        # initialisation de la fenetre
        self.setWindowTitle("Texte vers morse")
        self.ui = uic.loadUi('views/interface.ui')
        self.setFixedWidth(719)
        self.setFixedHeight(328)

        self.config = config(self)

        # récupération des éléments interactifs
        self.texteMorse = self.ui.findChildren(QTextEdit, 'texteMorse')[0]
        self.envoyer = self.ui.findChildren(QPushButton, 'envoyer')[0]
        effacer = self.ui.findChildren(QPushButton, 'effacer')[0]
        self.configuration = self.ui.findChildren(QPushButton, 'configuration')[0]
        quitter = self.ui.findChildren(QPushButton, 'quitter')[0]
        self.barreDeStatus = self.ui.findChildren(QLineEdit, 'barreDeStatus')[0]

        self.controller = ControllerMorse(self)

        self.setCentralWidget(self.ui)
        self.show()

        # liaison avec les controllers des boutons
        self.envoyer.clicked.connect(lambda checked: self.threadpool.start(self.controller))
        self.configuration.clicked.connect(lambda checked: self.config.show())
        effacer.clicked.connect(lambda checked: self.texteMorse.setText(""))
        quitter.clicked.connect(quit)

    def creerErreur(self, messageErreur):
        """
        Permet de générer une erreur critique. Lorsqu'on la ferme, le programme s'arrête.

        Parameters
        ----------
        messageErreur : str
            Le message qui sera affiché dans la fenêtre d'erreur. 
            Si le paramètre n'est pas de type str, "Vérifiez les logs" se met par défaut.
        """
        if not isinstance(messageErreur, str):
            messageErreur = "Vérifiez les logs."

        erreur = QMessageBox(QMessageBox.Critical, "Erreur", "Erreur critique", QMessageBox.Close)
        erreur.setInformativeText(messageErreur)
        ret = erreur.exec()
        if ret == QMessageBox.Close:
            self.close()
            self.threadpool.clear()
            exit()

if __name__ == '__main__':
    app = QApplication(argv)
    window = InterfaceMorse()
    exit(app.exec_())
