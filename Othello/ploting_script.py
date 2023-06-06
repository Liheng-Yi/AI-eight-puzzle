from Players import *
from GameDriver import GameDriver

import matplotlib.pyplot as plt

depths = [2, 4, 6, 8, 10, 12]
heuristics = [0, 1, 2]
pruning  = [0,1]
# Perform the searches and record the number of nodes seen
results = {}
for pruning in pruning:
    for depth in depths:
        for heuristic in heuristics:
            # Create a player for each heuristic
            GameDriver("alphabeta", "alphabeta", board_size, board_size, heuristic,
                    pruning, heuristic, pruning, depth, depth)




# # Plot the results
# for heuristic in heuristics:
#     nodes_seen = [results[(heuristic, depth)][0] for depth in depths]
#     plt.plot(depths, nodes_seen, label=f'Heuristic {heuristic}')


