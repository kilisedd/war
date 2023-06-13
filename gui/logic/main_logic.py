# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.forms.main_form import Ui_MainWindow
from gui.logic.virus_war import VirusForm


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.gameArea.setLayout(QtWidgets.QGridLayout())

        self.action_about.triggered.connect(self.about)
        self.action_Qt.triggered.connect(self.about_Qt)
        self.action_exit.triggered.connect(self.exit)
        self.toolBar.addAction(QtGui.QIcon(":/Icons/VirusWar.png"), "Война вирусов",
                               self.decorator_set_game(VirusForm))
        self.menu_2.insertActions(self.action_exit, self.toolBar.actions())
        self.menu_2.insertSeparator(self.action_exit)

        self.progressbar = QtWidgets.QProgressBar()
        self.statusbar.addPermanentWidget(self.progressbar)
        self.progressbar.setRange(0, 0)
        self.progressbar.hide()

    def decorator_set_game(self, game_form_class):
        def wrapper():
            return self.set_game(game_form_class)
        return wrapper

    def set_game(self, game_form_class):
        game_form: AbstractGameForm = game_form_class()
        if self.gameArea.layout().count() == 1:
            self.gameArea.layout().itemAt(0).widget().setParent(None)
        self.gameArea.layout().addWidget(game_form)
        game_form.resizeSignal.connect(self.resize)
        game_form.waitSignal.connect(self.show_progressbar)
        self.show_progressbar(False, 'Выберите параметры и начните игру')

    def show_progressbar(self, flag: bool, msg=None):
        if flag:
            self.progressbar.show()
            msg = msg or 'Подождите...'
            self.statusbar.showMessage(msg)
        else:
            self.progressbar.hide()
            msg = msg or 'Выберите клетку для хода'
            self.statusbar.showMessage(msg)

    def about(self):
        QtWidgets.QMessageBox.information(self, "О программе",
                                          "Программа разработана на языке Python при использовании библиотеки PyQt.",
                                          buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)

    def about_Qt(self):
        QtWidgets.QMessageBox.aboutQt(self)

    @staticmethod
    def exit():
        QtWidgets.qApp.quit()
