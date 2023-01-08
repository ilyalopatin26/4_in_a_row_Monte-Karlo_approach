from copy import deepcopy
import random
import numpy as np

from GameTable import *

class Node:
    def __init__(self, game_table):
        self.game_table = game_table
        self.children = [None for i in range(game_table.width)]
        #статистика
        self.win = 0
        self.lose = 0
        self.draw = 0
        self.init_children = False
    

class GameTree:
    def __init__(self, width, height, line_win, our_player, deep_force = 2, playout= 500,
                   only_ness_playout= True, dinamic_deep= True, max_deep = 4 , seed= 1  ):
        self.our_player = our_player
        self.dforce = deep_force
        self.playout = playout
        self.only_ness_playout = only_ness_playout
        self.dinamic_deep = dinamic_deep
        self.max_deep = max_deep
        
        self.dict_pos = {}
        self.cur_Node = Node( GameTable(width, height, line_win) )
        
        random.seed(seed)
        
    def init_children(self, Nodee):
        if Nodee.init_children:
            return
        Nodee.init_children = True
        pos_moves = Nodee.game_table.get_posibility_moves()
        for move in pos_moves:
            temp_GameTable = deepcopy(Nodee.game_table)
            temp_GameTable.make_move(move)
            temp_tuple = temp_GameTable.get_GameTable_to_tuples()
            temp_Node = self.dict_pos.get(temp_tuple, None)
            if not temp_Node :
                Nodee.children[move] = Node(temp_GameTable)
                self.dict_pos[temp_tuple] = Nodee.children[move]
            else:
                Nodee.children[move] = temp_Node
        

    def make_move(self, move):
        self.init_children(self.cur_Node)
        self.cur_Node = self.cur_Node.children[move]
    
        if self.dinamic_deep and self.dforce < self.max_deep:
            all_cell = self.cur_Node.game_table.width * self.cur_Node.game_table.height
            empty_cell = all_cell - len(self.cur_Node.game_table.stack_move)
            if empty_cell <=  all_cell / 2**( self.dforce + 1 ):
                self.dforce += 1

    def simulate(self, Nodee):
        """
        програть партию из Nodee
        1 - победил наш игрок
        0 - ничья
        -1 - победил противник
        """

        flag = Nodee.game_table.status()
        if flag != -1:
            if flag == 0:
                Nodee.draw += 1
                return 0
            if flag == self.our_player:
                Nodee.win += 1
                return 1
            else:
                Nodee.lose += 1
                return -1
        self.init_children(Nodee)

        if Nodee.game_table.garanted_win( Nodee.game_table.cur_player, 1 ):
            if Nodee.game_table.cur_player == self.our_player:
                Nodee.win += 1
                return 1
            else:
                Nodee.lose += 1
                return -1

        urgent_move = Nodee.game_table.urgent_move()
        
        pos_moves = Nodee.game_table.get_posibility_moves()
        
        rand_move = random.choice(pos_moves)
        if urgent_move != -1:
            rand_move = urgent_move
        ans = self.simulate(Nodee.children[rand_move])
        if ans == 1:
            Nodee.win += 1
        elif ans == 0:
            Nodee.draw += 1
        else:
            Nodee.lose += 1
        return ans

    def make_bot_move(self):

        def index(Nodee, all_playout):
            num_playout = Nodee.win + Nodee.lose + Nodee.draw
            if num_playout == 0:
                return 0
            return (Nodee.win + Nodee.draw / 2) / num_playout + np.sqrt(2 * np.log(all_playout) / num_playout)

        self.init_children(self.cur_Node)
        pos_moves = self.cur_Node.game_table.get_posibility_moves()
        random.shuffle(pos_moves)
        urgent_move = self.cur_Node.game_table.urgent_move()
        if len(pos_moves) == 1:
            self.make_move(pos_moves[0])
            return

        for move in pos_moves:
            if self.cur_Node.children[move].game_table.garanted_win(self.our_player, self.dforce):
                self.make_move(move)
                return
        
        if urgent_move != -1:
            self.make_move(urgent_move)
            return

        all_playout = 0
        for move in pos_moves:
            all_playout += self.cur_Node.children[move].win + self.cur_Node.children[move].lose + self.cur_Node.children[move].draw

        if (not self.only_ness_playout) or all_playout < self.playout:
            if self.only_ness_playout:
                for i in range(self.playout - all_playout):
                    self.simulate(self.cur_Node)
                all_playout = self.playout
            else:
                for i in range(self.playout):
                    self.simulate(self.cur_Node)
                all_playout = self.playout   

        best_move = pos_moves[0]
        best_index = index(self.cur_Node.children[best_move], all_playout)
        for move in pos_moves[1:]:
            temp_index = index(self.cur_Node.children[move], all_playout)
            if temp_index > best_index:
                best_index = temp_index
                best_move = move

        self.make_move(best_move)

