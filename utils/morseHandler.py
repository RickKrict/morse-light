##########
# IMPORT #
##########
import logging
from logging import Handler

######################
# INITIALISATION DES #
#     VARIABLES      #
######################
__author__ = "Rick"
__licence__ = "GPL3 or later"

class MorseHandler(Handler):
    def __init__(self, barreStatus):
        super(MorseHandler, self).__init__()
        self.barreStatus = barreStatus
        self.barreStatus.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.barreStatus.setText(msg)
        codeLog = record.levelno
        if codeLog == logging.INFO:
            self.barreStatus.setStyleSheet("QLineEdit { background: #33cc33 }")
        elif codeLog == logging.WARNING:
            self.barreStatus.setStyleSheet("QLineEdit { background: #ffff00 }")
        else:
            self.barreStatus.setStyleSheet("QLineEdit { background: #ff5050 }")

    def write(self, m): 
        pass
