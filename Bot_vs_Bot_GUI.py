import numpy as np
import pygame
import sys
import math

from GameTree import *
from parametrs import *


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

mainT1 = GameTree(COLUMN_COUNT, ROW_COUNT, LINE_WIN, 1, deep_force, playout, only_ness_playout, dinamic_deep, deep_force_max, seed)
mainT2 = GameTree(COLUMN_COUNT, ROW_COUNT, LINE_WIN, 2, deep_force, playout, only_ness_playout, dinamic_deep, deep_force_max, seed+1)

def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    board = mainT1.cur_Node.game_table.get_np_array()
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

pygame.init()

 
myfont = pygame.font.SysFont("monospace", 75)

game_over = False
turn = 1

while not game_over:        
    draw_board()
    pygame.display.update()
 
    flag = mainT1.cur_Node.game_table.status()

    if flag != -1:
        draw_board()
        pygame.display.update()
        if flag == 0:
            label = myfont.render("Draw", 1, RED)
            screen.blit(label, (40,10))
        else:
            label = myfont.render("Player {} wins!!".format(flag), 1, RED)
            screen.blit(label, (40,10))
        
        game_over = True
        pygame.display.update()
        pygame.time.wait(5000)
        sys.exit()

    if turn == 1:
        move = mainT1.make_bot_move()
        mainT2.make_move(move)
    
    else:
        move = mainT2.make_bot_move()
        mainT1.make_move(move)
    draw_board()
    pygame.display.update()
    turn = 3-turn

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
