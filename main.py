import sys
from WindowLogic import WindowLogic
import src_rc
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from PyQt5 import QtCore, QtGui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/logo/logo/hat.ico"))
    ui = WindowLogic()
    ui.show()
    sys.exit(app.exec_())