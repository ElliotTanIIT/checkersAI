from copy import deepcopy
import pygame
from checkers.constants import *

# position is a board object
# depth is depth of tree
# max_player is that it is trying for the maximum evaluation
# game is the current game object
def minimax(position, depth, max_player, ai_colour, player_colour, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, ai_colour, game):
            evaluation = minimax(move, depth-1, False, ai_colour, player_colour, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, player_colour, game):
            evaluation = minimax(move, depth-1, True, ai_colour, player_colour, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

# get all possible moves from current position
def get_all_moves(board, colour, game):
    # looks like [[board, piece], [board, piece]]. new board and piece that you move to get that new board.
    all_moves = []
    # for each piece, check all possible moves
    for piece in board.get_all_pieces(colour):
        valid_moves = board.get_valid_moves(piece)
        # move is a tuple (x, y), skip is the list of skipped pieces
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            # simulate the move and return the resulting potential board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            # save the potential board into all_moves
            all_moves.append(new_board)
    return all_moves

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board
    