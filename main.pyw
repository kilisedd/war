# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets

from gui.logic.main_logic import MainWindow



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    app.setStyle("Fusion")
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
