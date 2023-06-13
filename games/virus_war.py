# -*- coding: utf-8 -*-

from copy import deepcopy

import numpy as np

from games.abstracts import Piece, Board, Move


class Virus(Piece):
    def __init__(self, player: int, location: Move = None, is_dead: bool = False):
        super().__init__(player)
        self.is_dead = is_dead
        self.location = location

    @property
    def value(self):
        return self.is_dead + self.player if self.player < 2 else self.is_dead + self.player + 1

    def __repr__(self):
        return [' ', '□', '▣', '●', '◎'][self.value]


class Virus_war(Board):
    MAX_SCORES = 5

    def __init__(self, size: int = 8, turn: int = 1, field: np.ndarray = None,
                 pieces_lists: list[list[Virus]] = None, remaining_moves: int = 3, last_move: Move = None):
        self._size = size
        if field is None:
            field = np.array([[Virus(0, (i, j)) for j in range(self._size)] for i in range(self._size)], dtype=object)
            pieces_lists = [[], []]
            last_move = (0, self._size - 1)
        self._pieces_lists = pieces_lists
        self._field = field
        self._turn = turn
        self.remaining_moves = remaining_moves
        self.last_move = last_move
        self._legal_moves = self.get_moves_for_player(self.turn)

    def get_moves_for_player(self, player: int) -> set[Move]:
        checked = set()
        player_locs = [piece.location for piece in self._pieces_lists[player - 1]]
        moves = set()
        while player_locs:
            loc = player_locs.pop()
            checked.add(loc)
            for move in self.get_neighbours(loc):
                if (self._field[move] == self.last_turn and not self._field[move].is_dead) \
                        or self._field[move] == 0:
                    moves.add(move)
                elif self._field[move] == self.last_turn and self._field[move].is_dead \
                        and move not in checked:
                    player_locs.append(move)
        if (self._field == player).sum() == 0:
            moves = {(self._size - 1, 0)} if player == 1 else {(0, self._size - 1)}
        return moves

    def move(self, location: Move):
        if location not in self._legal_moves:
            raise (IndexError('Bad move (%d, %d)!' % location))
        x, y = location
        new_pieces_lists = deepcopy(self._pieces_lists)
        new_field = deepcopy(self._field)
        if new_field[x][y] == 0:
            new_field[x][y] = Virus(self.turn, location)
            new_pieces_lists[self.turn - 1].append(new_field[x][y])
        elif new_field[x][y] == self.last_turn:
            new_field[x][y].is_dead = True
            for i, piece in enumerate(new_pieces_lists[self.last_turn - 1]):
                if piece.location == location:
                    new_pieces_lists[self.last_turn - 1].pop(i)
                    break
        else:
            raise (IndexError('Bad move (%d, %d)!' % location))
        if self.remaining_moves == 1:
            new_turn = self.last_turn
            new_remaining_moves = 3
        else:
            new_turn = self.turn
            new_remaining_moves = self.remaining_moves - 1
        return Virus_war(self._size, new_turn, new_field, new_pieces_lists, new_remaining_moves, location)

    @property
    def is_win(self) -> bool:
        if len(self._legal_moves) == 0:
            return True
        return False

    @property
    def is_draw(self) -> bool:
        # There is no draw
        return False

    def evaluate(self, player: int) -> float:
        player_moves_count = len(self.get_moves_for_player(player))
        opponent = Piece().opposite(player)
        opponent_moves_count = len(self.get_moves_for_player(opponent))
        player_killed = 0
        opponent_killed = 0
        for i in range(self._size):
            for j in range(self._size):
                if self._field[i][j].is_dead:
                    if self._field[i][j] == opponent:
                        player_killed += 1
                    elif self._field[i][j] == player:
                        opponent_killed += 1
        return player_moves_count + player_killed * 5 - opponent_moves_count - opponent_killed * 5
