from copy import deepcopy
import pygame
from checkers.constants import *
from checkers.game import *

# position is a board object
# depth is depth of tree
# max_player is that it is trying for the maximum evaluation
# game is the current game object

def minimax(position, depth, max_player, alpha, beta, ai_colour, player_colour, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    if max_player:
        maxEval = NEG_INF
        best_move = None
        for move in get_all_moves(position, ai_colour, game):
            evaluation = minimax(move, depth-1, False, alpha, beta, ai_colour, player_colour, game)[0]
            maxEval = max(maxEval, evaluation)
            # update alpha value
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = POS_INF
        best_move = None
        for move in get_all_moves(position, player_colour, game):
            evaluation = minimax(move, depth-1, True, alpha, beta, ai_colour, player_colour, game)[0]
            minEval = min(minEval, evaluation)
            # update beta value
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
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
            #draw_moves(game, board, piece)
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
    
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, GREEN, (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100) #0.1 sec