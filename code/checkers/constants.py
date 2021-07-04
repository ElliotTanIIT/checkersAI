import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS # single '/' returns floating point, double '//' rounds down and returns int

#rgb colours
RED = (214, 36, 0) # going up
BIRCH = (248, 223, 161) # going down
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BAIGE = (171, 154, 108)

CROWN = pygame.transform.scale(pygame.image.load("checkers/assets/crown.png"), (44,25)) 