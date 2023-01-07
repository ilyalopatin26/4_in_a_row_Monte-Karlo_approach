class GameTable:
    def __init__(self, width_point, height_point , line_length_to_win ):
        self.array_points = [ [] for i in range(width_point)  ]
        self.width = width_point
        self.height = height_point
        self.len_win = line_length_to_win
    
    def check_posibility_move (self, num_line) :
        
        if len( self.array_points[num_line] ) < self.height:
            return True
        else:
            return False

    def get_array_posibility_move(self):
        return [i for i in range(self.width) if self.check_posibility_move(i)]

    def make_move(self, num_line, player):
        self.array_points[num_line].append(player)

    def check_horizontal(self, player):
        for i in range(self.width):
            count = 0
            for j in range( len(self.array_points[i]) ):
                if self.array_points[i][j] == player:
                    count += 1
                else:
                    count = 0
                if count == self.len_win:
                    return True
        return False

    def check_vertical(self, player):
        for i in range(self.height):
            count = 0
            for j in range(self.width):
                if len(self.array_points[j]) > i:
                    if self.array_points[j][i] == player:
                        count += 1
                    else:
                        count = 0
                else :
                    count = 0
                if count == self.len_win:
                    return True
        return False  

    def check_diagonal(self, player):
        for i in range(self.width):
            for j in range(self.height):
                count = 0
                for k in range(self.len_win):
                    if ( i+k >= self.width ) or ( j+k >= self.height ):
                        break
                    if len(self.array_points[i + k]) > j + k:
                        if self.array_points[i + k][j + k] == player:
                            count += 1
                        else:
                            count = 0
                    else:
                        count = 0
                    if count == self.len_win:
                        return True
        for i in range(self.width):
            for j in range(self.height):
                count = 0
                for k in range(self.len_win):
                    if ( i+k >= self.width ) or ( j-k < 0 ):
                        break
                    if len(self.array_points[i + k]) > j - k:
                        if self.array_points[i + k][j - k] == player:
                            count += 1
                        else:
                            count = 0
                    else:
                        count = 0        
                    if count == self.len_win:
                        return True

    def check_win(self, player):
        if self.check_horizontal(player) or self.check_vertical(player) or self.check_diagonal(player):
            return True
        else:
            return False

    def check_finish(self):
        for i in range(self.width):
            if self.check_posibility_move(i):
                return False
        return True
    
    def print_table(self):
        for h in range(self.height-1, -1, -1):
            for w in range(self.width):
                if len(self.array_points[w]) > h:
                    print(self.array_points[w][h], end = ' ')
                else:
                    print('_', end = ' ')
            print('\n')
        for i in range(self.width):
            print(i, end = ' ')
        print('\n')
    
    
    def check_game_over(self):
        for player in range(1, 3):
            if self.check_win(player):
                print('Player', player, 'win')
                return True
        if self.check_finish():
            print('Draw')
            return True
        else:
            return False

    def get_GameTable_to_tuples(self):
        return tuple([tuple(i) for i in self.array_points])

    def check_garented_win( self, player, num_our_player, deep_force) :
        if self.check_win(num_our_player):
            return True, 
        if self.check_win( 3-num_our_player ) or self.check_finish():
            return False
        if deep_force == 0:
            return False
        if player == num_our_player:
            for i in self.get_array_posibility_move():
                self.make_move(i, player)
                flag = True
                for j in self.get_array_posibility_move():
                    self.make_move(j, 3-player)
                    if not self.check_garented_win( player, num_our_player, 
                                                   deep_force-1):
                        flag = False
                        self.array_points[j].pop()
                        break
                    self.array_points[j].pop()
                if flag:
                    self.array_points[i].pop()
                    return True
                self.array_points[i].pop()
            return False
        else:
            flag = True
            for i in self.get_array_posibility_move():
                self.make_move(i, player)
                if self.check_garented_win(3-player, num_our_player, deep_force):
                    self.array_points[i].pop()
                else :
                    self.array_points[i].pop()
                    flag = False
                    break
            return flag
