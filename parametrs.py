#Game parameters, you can change them

#Game parameters
ROW_COUNT = 6   #number of rows
COLUMN_COUNT = 7    #number of columns
LINE_WIN = 4    #number of pieces in line to win
BOT_TURN = 1    #1 - bot starts, 2 - player starts

#Bot parameters
deep_force = 2  # start deep force of bot
deep_force_max = 4  # max deep force of bot
playout = 500  # number of playouts
only_ness_playout = True    # if True, bot will make playouts only if it is necessary
dinamic_deep = True # if True, bot will increase deep force if it is necessary
seed = 42   # seed for random


#For GUI, decrease it if you woud like to play on biggest game table
SQUARESIZE = 100