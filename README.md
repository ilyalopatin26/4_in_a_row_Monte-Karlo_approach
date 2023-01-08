# Four in a row with Monte-Karlo method

This project is denoted to experiments with the Monter-Karlo method of searching a game tree.
The main idea of it is that we semplays some number of games from the current position by making random moves and deciding on the best move based on the statistics data obtained.
This realization has several heuristics and chooses not quite random moves.

#### The first heuristic:
If the current player has a winning move, then it is chosen.

#### The second heuristic:
If the current player has a move that will lead to a winning move for the opponent, then it is chosen. This action prevents the opponent from winning the next move.    

## Method of picking a move
During the choice of a move, first, the possibility of a guaranteed win with a certain parameter of the depth of the total search is checked. The brute Forces parameter can be increased during the game. 
After that, the presence of an urgent move that prevents the opponent from winning on the next move is checked.
If there are no such moves, then the Monte-Karlo method is used.