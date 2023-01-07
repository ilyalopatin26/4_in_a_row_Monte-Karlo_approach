from copy import deepcopy
import random
import numpy as np

from GameTable import *

class Node:
    def __init__(self, game_table, player):
        self.game_table = game_table
        self.player = player
        self.children = [ None for i in range(game_table.width) ]
        self.number_win = 0
        self.number_draw = 0
        self.number_loss = 0



class GameTree :
    def __init__(self, width_point, height_point , line_length_to_win, 
                 num_our_player, deep_force=2,
                    num_playout=500, seed=42):
        self.curr_Node = Node(GameTable(width_point, height_point , 
                                        line_length_to_win), 1)
        self.num_our_player = num_our_player
        self.num_enemy_player = 3 - num_our_player
        self.width = width_point
        self.height = height_point
        self.len_win = line_length_to_win
        self.children = [None for i in range(width_point)]
        self.dict_pos = {}
        self.deep_force = deep_force #глубина перебора для выбора хода
        self.num_playout = num_playout #количество семплов партий из ноды
        
        random.seed(seed)

    
    def init_children_Node(self, Nodee ):
        for it in Nodee.game_table.get_array_posibility_move():
            if not Nodee.children[it]:
                temp_table = deepcopy(Nodee.game_table)
                temp_table.make_move(it, Nodee.player)
                temp_tuple = temp_table.get_GameTable_to_tuples()
                temp_Node = self.dict_pos.get( temp_tuple )
                if not temp_Node:
                    Nodee.children[it] = Node( temp_table, 3 - Nodee.player)
                    self.dict_pos[temp_tuple] = Nodee.children[it]
                else:
                    Nodee.children[it] = temp_Node

    def make_move(self, num_line):
        self.init_children_Node(self.curr_Node)
        self.curr_Node = self.curr_Node.children[num_line]



    def emulate_game(self, cur_Node ) :
        # 1 - win our player
        # 0 - draw
        # -1 - win enemy player

        # База рекурсии
        if cur_Node.game_table.check_win(self.num_our_player):
            return 1
        if cur_Node.game_table.check_win(self.num_enemy_player):
            return -1
        if cur_Node.game_table.check_finish():
            return 0

        self.init_children_Node(cur_Node)

        pos_move = cur_Node.game_table.get_array_posibility_move()

        if cur_Node.player != self.num_our_player :
            if cur_Node.game_table.check_garented_win( cur_Node.player,
                                                      self.num_enemy_player, 1):
                return -1
            rand_move = random.choice(pos_move)
            ans = self.emulate_game(cur_Node.children[rand_move])
            if ans == -1:
                cur_Node.number_loss += 1
            if ans == 0:
                cur_Node.number_draw += 1
            if ans == 1:
                cur_Node.number_win += 1
            return ans
        
        else:    
            if cur_Node.game_table.check_garented_win( cur_Node.player, 
                                        self.num_our_player, 1):
                return 1
            rand_move = random.choice(pos_move)
            ans = self.emulate_game(cur_Node.children[rand_move])
            if ans == -1:
                cur_Node.number_loss += 1
            if ans == 0:
                cur_Node.number_draw += 1
            if ans == 1:
                cur_Node.number_win += 1
            return ans
    
    def get_best_move(self):

        def get_index( Node, all_semplay ):
            all_sum = Node.number_draw + Node.number_loss + Node.number_win
            if all_sum == 0:
                return 0
            sum = (Node.number_win + Node.number_draw/2) / all_sum
            sum += np.sqrt(2 * np.log(all_semplay) / all_sum)
            return sum 

        
        for it in range(self.num_playout):
            self.emulate_game(self.curr_Node)
        pos_move = self.curr_Node.game_table.get_array_posibility_move()
        all_semplay = 0
        for it in pos_move:
            all_semplay += self.curr_Node.children[it].number_draw + self.curr_Node.children[it].number_loss + self.curr_Node.children[it].number_win
        first_Node = self.curr_Node.children[pos_move[0]]
        max_index = get_index(first_Node , all_semplay)
        best_move = pos_move[0]
        for it in pos_move:
            if self.curr_Node.children[it].game_table.check_garented_win( self.curr_Node.children[it].player, self.num_our_player, self.deep_force):
                return it
            if get_index(self.curr_Node.children[it], all_semplay) > max_index:
                max_index = get_index(self.curr_Node.children[it], all_semplay)
                best_move = it
        return best_move
