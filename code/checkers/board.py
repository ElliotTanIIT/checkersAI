import pygame
from .constants import *
from .piece import *

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.birch_left = 12
        self.red_kings = self.birch_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, BAIGE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # (pos x, pos y, width, height)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col%2 == ((row+1)%2):
                    # top rows with pieces
                    if row < 3:
                        self.board[row].append(Piece(row, col, BIRCH))
                    # bottom rows with pieces
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    # middle rows no pieces
                    else:
                        self.board[row].append(0) # no piece
                # all other squares no pieces
                else:
                    self.board[row].append(0) # no piece
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    

    def move(self, piece, row, col):
        # delete piece from current position and put it in a new position
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # check if move makes piece a king
        # pieces have to move in order for this to take effect, pieces starting at the ends won't have issues automatically becoming kings
        if row == ROWS - 1 or row == 0:
            # if its already a king, don't do anything
            if not piece.king:
                piece.make_king()
                if piece.colour == BIRCH:
                    self.birch_kings += 1
                else:
                    self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == RED:
                    self.red_left -= 1
                else:
                    self.birch_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return BIRCH
        elif self.birch_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        moves = {} # append to moves dict with (key, val) as ((pos x, pos y), [skipped pieces])
        # should check king first, then colour

        # check piece type

        # if king
        # check single moves (up and down)
        # check jumps (up and down)

        # if not king
        # check colour

        # if red
        # check single moves (up)
        # check jumps (up)

        # if birch
        # check single moves (down)
        # check jumps (down)

        
        if piece.king:
            moves.update(self.get_nojump_moves_king(piece.row, piece.col))
            moves.update(self.get_jump_moves_king(piece.row, piece.col, piece.colour))
        elif piece.colour == RED:
            moves.update(self.get_nojump_moves_red(piece.row, piece.col))
            moves.update(self.get_jump_moves_red(piece.row, piece.col, piece.colour))
        elif piece.colour == BIRCH:
            moves.update(self.get_nojump_moves_birch(piece.row, piece.col))
            moves.update(self.get_jump_moves_birch(piece.row, piece.col, piece.colour))
        
        return moves

    def get_nojump_moves_red(self, row, col):
        moves = {}
        row_up = row - 1
        col_left = col - 1
        col_right = col + 1
        if row_up >= 0:
            if col_left >= 0:
                if self.board[row_up][col_left] == 0:
                    moves.update({(row_up,col_left): []})
            if col_right < COLS:
                if self.board[row_up][col_right] == 0:
                    moves.update({(row_up,col_right): []})
        return moves

    def get_nojump_moves_birch(self, row, col):
        moves = {}
        row_down = row + 1
        col_left = col - 1
        col_right = col + 1
        if row_down < ROWS:
            if col_left >= 0:
                if self.board[row_down][col_left] == 0:
                    moves.update({(row_down, col_left): []})
            if col_right < COLS:
                if self.board[row_down][col_right] == 0:
                    moves.update({(row_down, col_right): []})
        return moves

    def get_nojump_moves_king(self, row, col):
        moves = {}
        row_up = row - 1
        row_down = row + 1
        col_left = col - 1
        col_right = col + 1
        # check all possible positions
        if row_up >= 0:
            if col_left >= 0:
                if self.board[row_up][col_left] == 0 and col_left >= 0:
                    moves.update({(row_up,col_left): []})
            if col_right < COLS:
                if self.board[row_up][col_right] == 0:
                    moves.update({(row_up,col_right): []})
        if row_down < ROWS:
            if col_left >= 0:
                if self.board[row_down][col_left] == 0:
                    moves.update({(row_down, col_left): []})
            if col_right < COLS:
                if self.board[row_down][col_right] == 0:
                    moves.update({(row_down, col_right): []})
        return moves
       
    def get_jump_moves_red(self, row, col, p_colour, skipped=[]):
        moves = {}
        row_up = row - 1
        col_left = col - 1
        col_right = col + 1
        if row_up >= 0: 
            # up left
            if col_left >= 0:
                if self.board[row_up][col_left] != 0 and self.board[row_up][col_left] not in skipped and (self.board[row_up][col_left]).colour != p_colour:
                    # check if the square you would jump to is also empty
                    # if it is, this is a valid move
                    if (row_up - 1) >= 0 and (col_left - 1) >= 0:
                        if self.board[row_up - 1][col_left - 1] == 0:
                            # update skipped list
                            next_skip = skipped + [self.board[row_up][col_left]]
                            # update moves
                            moves.update({(row_up - 1, col_left - 1): next_skip})
                            moves.update(self.get_jump_moves_red((row_up - 1), (col_left - 1), p_colour, skipped=next_skip))
            # up right
            if col_right < COLS:
                if self.board[row_up][col_right] != 0 and self.board[row_up][col_right] not in skipped and (self.board[row_up][col_right]).colour != p_colour:
                    if (row_up - 1) >= 0 and (col_right + 1) < COLS:
                        if self.board[row_up - 1][col_right + 1] == 0:
                            next_skip = skipped + [self.board[row_up][col_right]]
                            moves.update({(row_up - 1, col_right + 1): next_skip})
                            moves.update(self.get_jump_moves_red((row_up - 1), (col_right + 1), p_colour, skipped=next_skip))
        return moves

    def get_jump_moves_birch(self, row, col, p_colour, skipped=[]):
        moves = {}
        row_down = row + 1
        col_left = col - 1
        col_right = col + 1
        if row_down < ROWS: 
            # down left
            if col_left >= 0:
                if self.board[row_down][col_left] != 0 and self.board[row_down][col_left] not in skipped and col_left >= 0 and (self.board[row_down][col_left]).colour != p_colour:
                    if (row_down + 1) < ROWS and (col_left - 1) >= 0:
                        if self.board[row_down + 1][col_left - 1] == 0:
                            next_skip = skipped + [self.board[row_down][col_left]]
                            moves.update({(row_down + 1, col_left - 1): next_skip})
                            moves.update(self.get_jump_moves_birch((row_down + 1), (col_left - 1), p_colour, skipped=next_skip))
            # down right
            if col_right < COLS:
                if self.board[row_down][col_right] != 0 and self.board[row_down][col_right] not in skipped and col_right < COLS and (self.board[row_down][col_right]).colour != p_colour:
                    if (row_down + 1) < ROWS and (col_right + 1) < COLS: 
                        if self.board[row_down + 1][col_right + 1] == 0:
                            next_skip = skipped + [self.board[row_down][col_right]]
                            moves.update({(row_down + 1, col_right + 1): next_skip})
                            moves.update(self.get_jump_moves_birch((row_down + 1), (col_right + 1), p_colour, skipped=next_skip))
        return moves
    
    def get_jump_moves_king(self, row, col, p_colour, skipped=[]):
        moves = {}
        row_up = row - 1
        row_down = row + 1
        col_left = col - 1
        col_right = col + 1
        # check which adjacent squares have pieces that are opponent pieces
        if row_up >= 0: 
            # up left
            if col_left >= 0:
                if self.board[row_up][col_left] != 0 and self.board[row_up][col_left] not in skipped and (self.board[row_up][col_left]).colour != p_colour:
                    # check if the square you would jump to is also empty
                    # if it is, this is a valid move
                    if (row_up - 1) >= 0 and (col_left - 1) >= 0:
                        if self.board[row_up - 1][col_left - 1] == 0:
                            # update skipped list
                            next_skip = skipped + [self.board[row_up][col_left]]
                            # update moves
                            moves.update({(row_up - 1, col_left - 1): next_skip})
                            moves.update(self.get_jump_moves_king((row_up - 1), (col_left - 1), p_colour, skipped=next_skip))
            # up right
            if col_right < COLS:
                if self.board[row_up][col_right] != 0 and self.board[row_up][col_right] not in skipped and (self.board[row_up][col_right]).colour != p_colour:
                    if (row_up - 1) >= 0 and (col_right + 1) < COLS:
                        if self.board[row_up - 1][col_right + 1] == 0:
                            next_skip = skipped + [self.board[row_up][col_right]]
                            moves.update({(row_up - 1, col_right + 1): next_skip})
                            moves.update(self.get_jump_moves_king((row_up - 1), (col_right + 1), p_colour, skipped=next_skip))
        if row_down < ROWS: 
            # down left
            if col_left >= 0:
                if self.board[row_down][col_left] != 0 and self.board[row_down][col_left] not in skipped and col_left >= 0 and (self.board[row_down][col_left]).colour != p_colour:
                    if (row_down + 1) < ROWS and (col_left - 1) >= 0:
                        if self.board[row_down + 1][col_left - 1] == 0:
                            next_skip = skipped + [self.board[row_down][col_left]]
                            moves.update({(row_down + 1, col_left - 1): next_skip})
                            moves.update(self.get_jump_moves_king((row_down + 1), (col_left - 1), p_colour, skipped=next_skip))
            # down right
            if col_right < COLS:
                if self.board[row_down][col_right] != 0 and self.board[row_down][col_right] not in skipped and col_right < COLS and (self.board[row_down][col_right]).colour != p_colour:
                    if (row_down + 1) < ROWS and (col_right + 1) < COLS: 
                        if self.board[row_down + 1][col_right + 1] == 0:
                            next_skip = skipped + [self.board[row_down][col_right]]
                            moves.update({(row_down + 1, col_right + 1): next_skip})
                            moves.update(self.get_jump_moves_king((row_down + 1), (col_right + 1), p_colour, skipped=next_skip))

        return moves

    # scoring the board
    # positive: white winning
    # negtaive: red winning
    # tuning needed
    def evaluate(self):
        return self.birch_left - self.red_left + (self.birch_kings - self.red_kings)/2

    def get_all_pieces(self, colour):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)
        return pieces