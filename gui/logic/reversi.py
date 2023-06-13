# -*- coding: utf-8 -*-


from gui.logic.abstracts import *
from games.reversi import *


class ReversiCell(AbstractCell):

    ICONS = (None)
    INNER_COLOR1 = QtGui.QColor(200, 200, 200)
    INNER_COLOR2 = QtGui.QColor(250, 250, 250)
    OUTER_COLOR = QtGui.QColor(50, 50, 50)
    LAST_TURN_COLOR = QtGui.QColor(250, 0, 0)

    def paintEvent(self, *args, **kwargs):
        super(ReversiCell, self).paintEvent(*args, **kwargs)
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)
        if self.status == 1:
            pen = QtGui.QPen(self.LAST_TURN_COLOR)
            pen.setWidth(2)
            p.setPen(pen)
            p.drawRect(2, 2, self.SIZE - 4, self.SIZE - 4)


class ReversiForm(AbstractGameForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0, 'randomizing': 20}, 'Среднее': {'max_depth': 0, 'randomizing': 5},
                         'Сложно': {'max_depth': 0}}
    PLAYERS = ('Зелёные', 'Фиолетовые')
    RULES = "Война вирусов.\n\n" \
            "Игра для двух игроков, которая имитирует развитие двух колоний вирусов, которые развиваются сами и " \
            "уничтожают друг друга. В игре используется прямоугольная доска любых размеров.\nИгра начинается с " \
            "пустой доски. У каждого игрока имеется неограниченное кол-во 'вирусов' своего цвета: Зелёного и " \
            "Фиолетового.\nИгроки ходят по очереди. Начинает игрок, играющий Зелёными 'вирусами'.\nКаждый ход " \
            "состоит из трёх 'шагов'. Каждый 'шаг' является либо размножением, либо поглощением (убийство):\n " \
            "'размножение' - это выставление нового 'вируса' своего цвета в любую 'доступную' пустую клетку доски;" \
            "\n 'поглощение' - это 'убийство' одного из вирусов противника, находящегося на 'доступной' клетке. В " \
            "этом случае 'вирус' противника в клетке заменяется на специальную 'мёртвую' фишку цвета игрока. 'Убитые'" \
            " остаются неизменными на доске до конца партии, т.е. они не могут быть 'оживлены', 'восстановлены' или" \
            " удалены с доски.\nКлетка является 'доступной' в следующих случаях:\n - если клетка непосредственно " \
            "соприкасается (по вертикали, горизонтали или диагонали) с живым 'вирусом' игрока (даже, если этот " \
            "'вирус' был помещен на доску одним из предыдущих 'шагов' в течение того же хода);\n - если между " \
            "клеткой и 'вирусом' игрока, уже находящимся на доске, есть цепочка из 'убитых' вирусов противника, т.е." \
            " цепочка из соприкасающихся (по вертикали, горизонтали или диагонали) 'мертвых' вирусов цвета игрока " \
            "(даже, если эти вирусы были убиты в результате одного из предыдущих 'шагов' в течение того же хода).\n" \
            "Игрок обязан сделать все 3 'шага' каждый ход. Если игрок не может сделать очередной 'шаг', то он " \
            "проигрывает партию."
    Board_Class = Reversi
    Cell_Class = ReversiCell
    WIN_MESSAGE = ("Победил Зелёные!", "Победили фиолетовые!")

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(ReversiForm, self).__init__(parent)
        label = QtWidgets.QLabel('')
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label.setMaximumHeight(20)
        label.setObjectName('Scores')
        self.Scores = label
        self.boardFrame.layout().setSpacing(0)
        self.boardFrame.layout().addWidget(label, 1, 1)

    def renew_counter(self):
        y, p = self.party.board.get_gem_count
        if y > p:
            sign = '>'
        elif y < p:
            sign = '<'
        else:
            sign = '='
        self.Scores.setText('%s: %i %s %s: %i' % (self.PLAYERS[0], y, sign, self.PLAYERS[1], p))

    def update_values(self, field, legal_moves):
        super(ReversiForm, self).update_values(field, legal_moves)
        if self.party.board.last_move:
            x, y = self.party.board.last_move
            self.boardField.itemAtPosition(x, y).widget().status = 1
            self.boardField.itemAtPosition(x, y).widget().update()
        self.renew_counter()
