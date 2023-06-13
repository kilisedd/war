# -*- coding: utf-8 -*-


from games.virus_war import *
from gui.logic.reversi import *


class VirusCell(ReversiCell):
    ICONS = (None, ":/Icons/greenVirus.png", ":/Icons/greenDeadVirus.png",
             ":/Icons/purpleVirus.png", ":/Icons/purpleDeadVirus.png")
    INNER_COLOR1 = QtGui.QColor(150, 250, 250)
    INNER_COLOR2 = QtGui.QColor(150, 200, 250)
    OUTER_COLOR = QtGui.QColor(0, 0, 0)
    LAST_TURN_COLOR = QtGui.QColor(250, 0, 0)


class VirusForm(ReversiForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0, 'randomizing': 20}, 'Среднее': {'max_depth': 0, 'randomizing': 5},
                         'Сложно': {'max_depth': 0}}
    BOARD_SIZES = ('10','11', '12')
    PLAYERS = ('Зелёные', 'Фиолетовые')
    Board_Class = Virus_war
    Cell_Class = VirusCell

    WIN_MESSAGE = ("Победили зелёные!", "Победили фиолетовые!")

    def renew_counter(self):
        pass
