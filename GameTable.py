import numpy as np

class GameTable :
    def __init__(self, width, height, line_win):
        self.width = width
        self.height = height
        self.line_win = line_win
        self.table = [ [] for i in range(self.width) ]
        self.cur_player = 1
        self.stack_move = []

    def check_posibility_move(self, num_line):
        return bool(len(self.table[num_line]) < self.height)
    
    def get_posibility_moves(self):
        return [i for i in range(self.width) if self.check_posibility_move(i)]
    
    def get_opponent(self):
        return 3 - self.cur_player
    
    def make_move(self, move):
        self.table[move].append(self.cur_player)
        self.stack_move.append(move)
        self.cur_player = self.get_opponent()
    
    def undo_move(self):
        move = self.stack_move.pop()
        self.table[move].pop()
        self.cur_player = self.get_opponent()
    
    def check_win(self):
        # check that last move is win

        def check_vertical():
            last_move = self.stack_move[-1]
            if len(self.table[last_move]) < self.line_win:
                return False
            for i in range(self.line_win):
                if self.table[last_move][-i-1] != self.get_opponent():
                    return False
            return True
        
        def check_horizontal():
            last_move = self.stack_move[-1]
            top = len(self.table[last_move]) -1
            #two pointer method
            left = last_move
            right = last_move
            while left > 0 and len(self.table[left-1]) > top:
                if self.table[left-1][top] != self.get_opponent():
                    break
                left -= 1
            while right < self.width - 1 and len(self.table[right+1]) >top:
                if self.table[right+1][top] != self.get_opponent():
                    break
                right += 1
            return bool(right-left+1 >= self.line_win)
        
        def check_diagonal():
            last_move = self.stack_move[-1]

            #diagonal up to the left
            top = len(self.table[last_move]) -1
            left = last_move
            right = last_move
            while left > 0 and top > 0 and len(self.table[left-1]) > top-1 :
                if self.table[left-1][top-1] != self.get_opponent():
                    break
                left -= 1
                top -= 1
            top = len(self.table[last_move]) -1
            while right < self.width - 1 and top < self.height - 1 and len(self.table[right+1]) > top+1:
                if self.table[right+1][top+1] != self.get_opponent():
                    break
                right += 1
                top += 1
            if right-left+1 >= self.line_win:
                return True
            
            #diagonal up to the left
            top = len(self.table[last_move]) -1
            left = last_move
            right = last_move
            while left > 0 and top < self.height - 1 and len(self.table[left-1]) > top+1 :
                if self.table[left-1][top+1] != self.get_opponent():
                    break
                left -= 1
                top += 1
            top = len(self.table[last_move]) -1
            while right < self.width - 1 and top > 0 and len(self.table[right+1]) > top-1:
                if self.table[right+1][top-1] != self.get_opponent():
                    break
                right += 1
                top -= 1
            if right-left+1 >= self.line_win:
                return True
            return False

        if len(self.stack_move) == 0:
            return False
        return check_vertical() or check_horizontal() or check_diagonal()

    def check_draw(self):
        return bool(len(self.stack_move) == self.width * self.height)
    
    def status(self):
        """
        -1 - game is not over
        0 - draw
        1 - win first player
        2 - win second player
        """
        if self.check_win():
            return self.get_opponent()
        if self.check_draw():
            return 0
        return -1
    
    def print_table(self):
        for h in range(self.height-1, -1, -1):
            for w in range(self.width):
                if len(self.table[w]) > h:
                    print(self.table[w][h], end = ' ')
                else:
                    print('_', end = ' ')
            print('\n')
        for i in range(self.width):
            print(i, end = ' ')
        print('\n')
    
    def get_GameTable_to_tuples(self):
        return tuple([tuple(i) for i in self.table])

    def guaranteed_win(self, target_player, deep):
        """
        check that the target_player can win for his moves and 
        any answers of the opponent
        """

        flag = self.status()
        if flag != -1:
            return bool(flag == target_player)
        if deep == 0:
            return False
        
        pos_moves = self.get_posibility_moves()
        if self.cur_player == target_player:
            for move in pos_moves:
                self.make_move(move)
                if self.guaranteed_win(target_player, deep-1):
                    self.undo_move()
                    return True
                self.undo_move()
            return False
        else:
            flag = True
            for move in pos_moves:
                self.make_move(move)
                if not self.guaranteed_win(target_player, deep):
                    self.undo_move()
                    flag = False
                    break
                self.undo_move()
            return flag
            
    def urgent_move(self):
        """
        urgent move -- a move that allows you to win in one move for your opponent, 
        if we don't make it ourselves.

        returns -1 if there is no such move
        Otherwise, it returns the column number
        """

        self.cur_player = self.get_opponent()
        pos_moves = self.get_posibility_moves()
        for move in pos_moves:
            self.make_move(move)
            if self.status() == self.get_opponent():
                self.undo_move()
                self.cur_player = self.get_opponent()
                return move
            self.undo_move()
        self.cur_player = self.get_opponent()
        return -1
    
    def get_np_array(self):
        """
        returns a numpy array with the game table
        """
        np_array = np.zeros((self.height, self.width))
        for w in range(self.width):
            for h in range(self.height):
                if len(self.table[w]) > h:
                    np_array[h][w] = self.table[w][h]
                else:
                    np_array[h][w] = 0
        return np_array
