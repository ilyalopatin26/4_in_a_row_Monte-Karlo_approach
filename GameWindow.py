import numpy as np
import pygame
import sys
import math

from GameTree import *
from parametrs import *


BLUE = (0,0,255)
BLACK = ( 0, 0 ,0)
RED = (255,0,0)
YELLOW = (255,255,0)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
mainT = GameTree(COLUMN_COUNT, ROW_COUNT, LINE_WIN, BOT_TURN, deep_force, playout, only_ness_playout, dinamic_deep, deep_force_max, seed)

def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    board = mainT.cur_Node.game_table.get_np_array()
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def game_end():
    flag = mainT.cur_Node.game_table.status()
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    pygame.display.update()
    draw_board()
    pygame.display.update()
    if flag == 0:
        label = myfont.render("Draw", 1, RED)
        screen.blit(label, (40,10))
    else:
        label = myfont.render( f'Player { flag } wins', 1, RED)
        screen.blit(label, (40,10))
    pygame.display.update()
    pygame.time.wait(5000)
    sys.exit()

pygame.init()

 
myfont = pygame.font.SysFont("monospace", 75)

game_over = False
turn = 1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        draw_board()
        pygame.display.update()
 
        flag = mainT.cur_Node.game_table.status()

        if flag != -1:
            game_end()

        if turn == BOT_TURN:
            mes = myfont.render("Bot's turn", 1, RED)
            screen.blit(mes, (40,10))
            pygame.display.update()
            mainT.make_bot_move()
            turn = 3-turn
            break

    
        else:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn != BOT_TURN:
                    if turn == 1:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            draw_board()
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN :
                flag_complete_bot_move = False
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
 
                if mainT.cur_Node.game_table.check_posibility_move(col):
                    mainT.make_move(col)
                    turn = 3-turn
            break
