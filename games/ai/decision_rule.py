# -*- coding: utf-8 -*-
"""A set of functions for making a decision by the computer during the selection of a move"""

from random import shuffle, randint

from games.abstracts import *


def alphabeta(board: Board, original_player: int, depth: int = 8,
              alpha: float = float('-inf'), beta: float = float('inf')) -> float:
    if board.is_draw:
        return 0
    if board.is_win or depth == 0:
        # If max depth is reached then stop and return current evaluate of scores for player.
        return board.evaluate(original_player)
    if board.turn == original_player:
        # Player want to do best move and max his scores.
        for move in board.legal_moves:
            # There will be next level of depth.
            scores = alphabeta(board.move(move), original_player, depth-1, alpha, beta)
            alpha = max(scores, alpha)
            if alpha >= beta:
                break
        return alpha
    else:
        # Opponent want to do best move and min player's scores.
        for move in board.legal_moves:
            # There will be next level of depth.
            scores = alphabeta(board.move(move), original_player, depth-1, alpha, beta)
            beta = min(scores, beta)
            if alpha >= beta:
                break
        return beta


def find_best_move(board: Board, max_depth: int = 0, randomizing: int = 0) -> Union[Move, tuple[Move, Move]]:
    """
    Uses MiniMax and AlphaBeta algorithms to select best move.

    :param board: Current state of game
    :param max_depth: How deep to provide a search
    :param randomizing: Computers moves will be less logic (easier difficulty).
    :return: Move with maximum estimated scores
    """
    player = board.turn
    moves = board.legal_moves
    shuffle(moves)
    best_scores = float('-inf')
    best_move = moves[0]
    for move in moves:
        scores = alphabeta(board.move(move), player, max_depth, alpha=best_scores)
        if randomizing:
            scores = scores + (board.MAX_SCORES - scores) * randint(0 + randomizing//2, 0 + randomizing) / 20
        # print(move, scores)
        if scores > best_scores:
            best_move = move
            best_scores = scores
    return best_move

