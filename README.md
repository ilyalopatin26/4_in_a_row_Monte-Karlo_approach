# Four in a row with Monte-Karlo method

This project is denoted to experiments with the Monter-Karlo method of searching a game tree.
The main idea is that we semplays some number of games from the current position by making random moves and deciding on the best move based on the statistics data obtained.
![alt text](./MCTS_general.png "Monte-Karlo method")

This realization has several heuristics and chooses not quite random moves during simulation.

#### The first heuristic:
If the current player has a winning move, then it is chosen.

#### The second heuristic:
If the current player has a move that will lead to a winning move for the opponent( such moves are called urgent moves in this projct code), then it is chosen. This action prevents the opponent from winning the next move.    

## Method of picking a move
During the choice of a move, first, the possibility of a guaranteed win with a certain parameter of the depth of the total search is checked. The brute Forces parameter can be increased during the game. 
After that, the presence of an urgent move that prevents the opponent from winning on the next move is checked.
If there are no such moves, then the Monte-Karlo method is used.

## How to run
To run the program, you need to have installed python 3.6 or higher.
Then you need to install the pygame library and numpy.

File parameters.py contains the parameters of the game and bot, see coments in file. You can change them. 

For playing against bot run GameWindow.py. For bot vs bot game run Bot_vs_Bot_GUI.py.
