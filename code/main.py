import pygame

from checkers.constants import *
from checkers.board import *
from checkers.game import *
from minimax.algorithm import *

FPS = 60
ai_colour = BIRCH
player_colour = RED
max_player = BIRCH
#window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.turn == ai_colour:
            value, new_board = minimax(game.get_board(), MINIMAX_DEPTH, max_player, NEG_INF, POS_INF, ai_colour, player_colour, game)
            game.ai_move(new_board)
        if game.winner() != None:
            print(game.winner())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                game.select(row, col)
        
        game.update()
            
    pygame.quit()
        
main()