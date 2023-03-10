from copy import deepcopy
import random
import numpy as np

from GameTable import *

class Node:
    def __init__(self, game_table):
        self.game_table = game_table
        self.children = [None for i in range(game_table.width)]
        self.init_children = False
        
        #statistic
        self.win = 0
        self.lose = 0
        self.draw = 0
        
class GameTree:
    def __init__(self, width, height, line_win, our_player, deep_force, playout,
                   only_ness_playout, dinamic_deep, max_deep, seed ):
        self.our_player = our_player
        self.dforce = deep_force
        self.playout = playout
        self.only_ness_playout = only_ness_playout
        self.dinamic_deep = dinamic_deep
        self.max_deep = max_deep
        
        self.dicts_pos = [ {} for i in range(width*height+1) ]
        self.cur_Node = Node( GameTable(width, height, line_win) )
        
        temp_tuple = self.cur_Node.game_table.get_GameTable_to_tuples()
        self.dicts_pos[0][temp_tuple] = self.cur_Node

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
            temp_Node = self.dicts_pos[len(temp_GameTable.stack_move)].get(temp_tuple)
            if not temp_Node :
                Nodee.children[move] = Node(temp_GameTable)
                self.dicts_pos[len(temp_GameTable.stack_move)][temp_tuple] = Nodee.children[move]
            else:
                Nodee.children[move] = temp_Node
        

    def make_move(self, move):
        self.init_children(self.cur_Node)
        self.cur_Node = self.cur_Node.children[move]
    
        if self.dinamic_deep and self.dforce < self.max_deep:
            all_cell = self.cur_Node.game_table.width * self.cur_Node.game_table.height
            empty_cell = all_cell - len(self.cur_Node.game_table.stack_move)
            if empty_cell <=  all_cell / 2**( self.dforce):
                self.dforce += 1

    def simulate(self, Nodee):
        """
        simulate game from Nodee
        return 1 if win, 0 if draw, -1 if lose
        """

        flag = Nodee.game_table.status()
        if flag != -1:
            if flag == 0:
                Nodee.draw += 1
                return 0
            elif flag == self.our_player:
                Nodee.win += 1
                return 1
            else:
                Nodee.lose += 1
                return -1
        self.init_children(Nodee)

        if Nodee.game_table.guaranteed_win( Nodee.game_table.cur_player, 1 ):
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
            #return index winrate of Nodee
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
            return pos_moves[0]

        for move in pos_moves:
            if self.cur_Node.children[move].game_table.guaranteed_win(self.our_player, self.dforce):
                self.make_move(move)
                return move
        
        if urgent_move != -1:
            self.make_move(urgent_move)
            return urgent_move

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
        return best_move

