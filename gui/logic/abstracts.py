# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui

from basic.party import *
from games.abstracts import Board
from gui.forms.game_form import Ui_GameForm


class AbstractCell(QtWidgets.QWidget):
    SIZE = 40
    ICONS = (None, ":/Icons/cross.png", ":/Icons/naught.png")
    OUTER_COLOR = QtGui.QColor(200, 200, 200)
    HELP_COLOR = QtGui.QColor(225, 200, 0)
    INNER_COLOR1 = QtGui.QColor(50, 50, 50)
    INNER_COLOR2 = QtGui.QColor(200, 225, 200)

    clicked = QtCore.pyqtSignal(int, int)

    def __init__(self, x: int, y: int, value: int, *args, **kwargs):
        super(AbstractCell, self).__init__(*args, **kwargs)
        self.setFixedSize(QtCore.QSize(self.SIZE, self.SIZE))

        self.x = x
        self.y = y
        self.value = value
        self.isAvailable = True
        self.status = 0

    def paintEvent(self, event: QtGui.QPaintEvent):
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)

        r = event.rect()
        if (self.x + self.y) % 2:
            inner_color = self.INNER_COLOR1
        else:
            inner_color = self.INNER_COLOR2
        brush = QtGui.QBrush(inner_color)
        p.fillRect(r, brush)
        pen = QtGui.QPen(inner_color)
        if self.isAvailable:
            pen = QtGui.QPen(self.HELP_COLOR)
        pen.setWidth(2)
        p.setPen(pen)
        p.drawRect(2, 2, self.SIZE - 4, self.SIZE - 4)
        pen = QtGui.QPen(self.OUTER_COLOR)
        pen.setWidth(2)
        p.setPen(pen)
        p.drawRect(r)
        image = self.ICONS[self.value]
        if image:
            p.drawPixmap(r, QtGui.QPixmap(image))

    def mouseReleaseEvent(self, event):
        if self.isAvailable:
            self.clicked.emit(self.x, self.y)


class AbstractGameForm(QtWidgets.QWidget, Ui_GameForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0}, 'Среднее': {'max_depth': 1}, 'Сложно': {'max_depth': 3}}
    # BOARD_SIZES = ('8',)
    PLAYERS = ('Белые', 'Чёрные')
    RULES = "Здесь могла быть выша игра."
    WIN_MESSAGE = ("Победили белые!", "Победили чёрные!")
    Board_Class = Board
    Cell_Class = AbstractCell

    resizeSignal = QtCore.pyqtSignal(int, int)
    waitSignal = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(AbstractGameForm, self).__init__(parent)
        self.setupUi(self)
        self.party = None
        self.size = None
        self.setup_form()
        self.blocked = False

    def setup_form(self):
        self.difficultyLevelsCombo.addItems(self.DIFFICULTY_LEVELS.keys())
        self.sizesCombo.addItems(self.BOARD_SIZES)
        self.computerPlayerCombo.addItems(self.PLAYERS)
        self.rulesText.setText(self.RULES)
        self.startButton.clicked.connect(self.game_start)

    def game_start(self):
        is_AI = self.isComputer.isChecked()
        difficulty_settings = self.DIFFICULTY_LEVELS[self.difficultyLevelsCombo.currentText()]
        self.size = int(self.sizesCombo.currentText())
        AI_player = self.computerPlayerCombo.currentIndex() + 1
        board = self.Board_Class(turn=1, size=self.size)
        self.party = Party(board, is_AI, AI_player, difficulty_settings)
        self.party.sendGameField.connect(self.update_values)
        self.party.sendGameState.connect(self.update_state)
        self.party.unblockGameForm.connect(self.unblocking)
        self.party.waitSignal.connect(self.emit_waiting)

        self.boardField.setSpacing(0)
        for i in reversed(range(self.boardField.count())):
            self.boardField.itemAt(i).widget().setParent(None)
        for i in range(self.size):
            for j in range(self.size):
                w = self.Cell_Class(i, j, board.get_value(i, j))
                w.clicked.connect(self.apply_move)
                self.boardField.addWidget(w, i, j)
        self.party.start(None)
        size = self.boardField.itemAtPosition(0, 0).widget().SIZE
        width = self.size * size + 50 + self.settingsFrame.width()
        height = self.size * size + 140
        self.resizeSignal.emit(width, height)

    def is_available_move(self, move, legal_moves):
        return move in legal_moves

    def update_values(self, field, legal_moves):
        legal_moves = set(legal_moves)
        for i in reversed(range(self.boardField.count())):
            w = self.boardField.itemAt(i).widget()
            value = field[w.x][w.y].value
            w.value = value
            w.status = 0
            if self.is_available_move((w.x, w.y), legal_moves):
                w.isAvailable = True
            else:
                w.isAvailable = False
            w.update()

    def apply_move(self, x, y):
        self.waitSignal.emit(True, None)
        if not self.blocked:
            self.party.start((x, y))
            self.blocked = True

    def unblocking(self):
        self.blocked = False

    def emit_waiting(self, flag: bool, msg: str = None):
        self.waitSignal.emit(flag, msg)

    def update_state(self, status_code: int):
        if status_code:
            for i in reversed(range(self.boardField.count())):
                w = self.boardField.itemAt(i).widget()
                w.isAvailable = False
                w.status = 0
            if status_code == DRAW:
                QtWidgets.QMessageBox.information(self,
                                                  "Ничья!",
                                                  "Никто не победил!",
                                                  buttons=QtWidgets.QMessageBox.Ok)
                self.emit_waiting(False, "Ничья!")
            elif status_code == BAD_MOVE:
                QtWidgets.QMessageBox.warning(self,
                                              "Невозможный ход!",
                                              "Данный ход нельзя совершить! Выберите другой ход!",
                                              buttons=QtWidgets.QMessageBox.Ok)
            else:
                if self.party.isAI and status_code == self.party.AI_player:
                    text = "Победил компьютер!"
                else:
                    text = self.WIN_MESSAGE[status_code - 1]
                QtWidgets.QMessageBox.information(self,
                                                  "Конец игры!",
                                                  text,
                                                  buttons=QtWidgets.QMessageBox.Ok)
                self.emit_waiting(False, text)
