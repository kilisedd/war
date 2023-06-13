# -*- coding: utf-8 -*-

import numpy as np

from games.abstracts import Piece, Board, Move


class Figure(Piece):
    NUM2STR = ['0', '+', '-']


class Reversi(Board):

    def __init__(self, size: int = 15, turn: int = 1, field: np.ndarray = None, boundary_moves: set = None,
                 last_move: Move = None):
        if field is None:
            field = np.array([[Figure(0) for _ in range(size)] for _ in range(size)], dtype=object)
            field[size // 2 - 1][size // 2 - 1] = Figure(1)
            field[size // 2][size // 2] = Figure(1)
            field[size // 2 - 1][size // 2] = Figure(2)
            field[size // 2][size // 2 - 1] = Figure(2)
            boundary_moves = {(i, j) for i in range(size // 2 - 2, size // 2 + 2)
                              for j in range(size // 2 - 2, size // 2 + 2) if field[i][j] == 0}
        self._field = field
        self._size = size
        self._turn = turn
        self._boundary_moves = boundary_moves
        self._legal_moves = []
        self._gem_counters = [0, 0, 0]
        self.last_move = last_move
        for i in range(3):
            self._gem_counters[i] = (self._field == i).sum()
        self.check_legal_moves()
        if len(self._legal_moves) == 0:
            self._turn = self.last_turn
            self.check_legal_moves()
        if len(self._legal_moves) == 0:
            self._gem_counters[0] = 0

    @property
    def get_gem_count(self):
        return self._gem_counters[1], self._gem_counters[2]

    def check_legal_moves(self):
        self._legal_moves = []
        for x, y in self._boundary_moves:
            move_added = False
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                k = 1
                next_x, next_y = x + k * dx, y + k * dy
                got_reverse_color = False
                while 0 <= next_x < self._size and 0 <= next_y < self._size and self._field[next_x][next_y] != 0:
                    if self._field[next_x][next_y] == self.last_turn:
                        got_reverse_color = True
                    else:
                        if self._field[next_x][next_y] == self.turn and got_reverse_color:
                            self._legal_moves.append((x, y))
                            move_added = True
                        break
                    k += 1
                    next_x, next_y = x + k * dx, y + k * dy
                if move_added:
                    break

    def move(self, location: Move):
        if location not in self._legal_moves:
            raise (IndexError('Current location (%d, %d) is already occupied' % location))
        x, y = location
        new_boundary_moves = self._boundary_moves.copy()
        for i, j in self.get_neighbours((x, y)):
            if 0 <= i < self._size and 0 <= j < self._size and self._field[i][j] == 0:
                new_boundary_moves.add((i, j))
        new_boundary_moves.remove((x, y))
        new_field = self._field.copy()
        new_field[x][y] = Figure(self.turn)
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            k = 1
            next_x, next_y = x + k * dx, y + k * dy
            got_reverse_color = False
            while 0 <= next_x < self._size and 0 <= next_y < self._size and self._field[next_x][next_y] != 0:
                if self._field[next_x][next_y] == self.last_turn:
                    got_reverse_color = True
                else:
                    if self._field[next_x][next_y] == self.turn and got_reverse_color:
                        next_x -= dx
                        next_y -= dy
                        while next_x != x or next_y != y:
                            new_field[next_x][next_y] = Figure(self.turn)
                            next_x -= dx
                            next_y -= dy
                    break
                k += 1
                next_x, next_y = x + k * dx, y + k * dy
        new_turn = self.last_turn
        return Reversi(self._size, new_turn, new_field, new_boundary_moves, location)

    @property
    def is_win(self) -> bool:
        if self._gem_counters[0] == 0:
            if self._gem_counters[1] > self._gem_counters[2]:
                self._turn = 2
                return True
            if self._gem_counters[2] > self._gem_counters[1]:
                self._turn = 1
                return True
        return False

    @property
    def is_draw(self) -> bool:
        if self._gem_counters[0] == 0:
            return self._gem_counters[1] == self._gem_counters[2]
        return False

    def evaluate(self, player: int) -> float:
        return self._gem_counters[player] - self._gem_counters[Piece.opposite(player)]
