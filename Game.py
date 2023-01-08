from GameTree import *


width_point = 7
height_point = 6 
line_length_to_win = 4 

num_bot_player = 1
cur_player = 1

mainT = GameTree(width_point, height_point, line_length_to_win, num_bot_player)

while True:

    mainT.cur_Node.game_table.print_table()

    temp = mainT.cur_Node.game_table.status()
    if temp != -1:
        if temp == 0:
            print("Draw")
        else:
            print("Player {} win".format(temp))
        break

    if cur_player != num_bot_player:
        print("Your move")
        num_line = int(input())
        if num_line in mainT.cur_Node.game_table.get_posibility_moves():
            mainT.make_move(num_line)
            cur_player = 3 - cur_player
        else:
            print("Error")
            break

    else:
        print("Bot move")
        mainT.make_bot_move()
        cur_player = 3 - cur_player
        
