from Node import *


width_point = 7
height_point = 6 
line_length_to_win = 4 

num_bot_player = 2
cur_player = 1

mainT = GameTree(width_point, height_point, line_length_to_win, num_bot_player)

while True:

    mainT.curr_Node.game_table.print_table()

    temp = mainT.curr_Node.game_table.check_game_over()
    if temp:
        break

    if cur_player != num_bot_player:
        num_line = int(input())
        if num_line in mainT.curr_Node.game_table.get_array_posibility_move():
            mainT.make_move(num_line)
            cur_player = 3 - cur_player
        else:
            print("Error")
            break

    else:
        print("Bot move")
        best_move = mainT.get_best_move()
        mainT.make_move(best_move)
        cur_player = 3 - cur_player
        
