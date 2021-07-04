import pygame
from .constants import *

class Piece:
    PADDING = 12
    OUTLINE = 1
    def __init__ (self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.king = False
        self.x = self.y = 0
        self.calc_pos()

    # calculate location based on row and column
    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2
    
    def make_king(self):
        self.king = True
    
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.colour, (self.x, self.y), radius+self.OUTLINE)
        pygame.draw.circle(win, self.colour, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x-(CROWN.get_width()//2), self.y-(CROWN.get_height()//2)))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def make_king(self):
        self.king = True

    def __repr__(self):
        return str(self.colour)