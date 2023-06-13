# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union

import numpy as np

Move = tuple[10, 10]


class Piece:
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    NUM2STR = ['_', 'X', '0']

    def __init__(self, player: int = 0):
        self.player = player

    @staticmethod
    def opposite(player: int) -> int:
        """Returns the opposite player number."""
        return 1 + player % 2

    @property
    def value(self):
        return self.player

    def __eq__(self, other):
        return self.player == other

    def __index__(self):
        return self.player

    def __repr__(self):
        return self.NUM2STR[self.player]


class Board(ABC):
    MAX_SCORES = 100

    @abstractmethod
    def __init__(self, turn: int = 1, size: int = 8, field: Union[list[list[Piece]], np.ndarray] = None):
        if field is None:
            pass
        self._field = field
        self._size = size
        self._turn = turn
        self._legal_moves = set()

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def field(self):
        return self._field

    @property
    def last_turn(self) -> int:
        """Returns number of previous player."""
        return Piece.opposite(self._turn)

    def get_neighbours(self, location: Move, area_size: int = 1) -> list[Move]:
        """Returns a list of adjacent locations."""
        x, y = location
        neighbours = ((x - i, y - j) for i in range(-area_size, area_size + 1)
                      for j in range(-area_size, area_size + 1))
        possible_neighbours = [(x, y) for x, y in neighbours if 0 <= x < self._size and 0 <= y < self._size]
        return possible_neighbours

    @abstractmethod
    def move(self, location: Union[Move, tuple[Move, Move]]) -> Board:
        """
        Returns board with next state after move.

        :param location:
        :return: copy of board with new state
        """
        pass

    @property
    @abstractmethod
    def is_win(self) -> bool:
        """Returns True if player wins."""
        pass

    @property
    def is_draw(self) -> bool:
        """Returns True if there are no moves and no one wins."""
        return not (self.is_win or self.legal_moves)

    @property
    def legal_moves(self) -> Union[list[Move], list[tuple[Move, Move]]]:
        """Returns list of possible and reasonable moves. It's necessary for ai."""
        return list(self._legal_moves)

    @abstractmethod
    def evaluate(self, player: int) -> float:
        """Evaluate state of board for current player and returns estimation of scores. It's necessary for ai."""
        pass

    def get_value(self, x: int, y: int) -> int:
        """Returns value from field"""
        return self._field[x][y].value

    def __str__(self):
        return self._field.__str__()
