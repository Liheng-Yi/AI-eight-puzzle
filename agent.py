from __future__ import annotations
from board import Board
from collections.abc import Callable
from queue import PriorityQueue
import numpy as np

'''
Heuristics
'''
def MT(board: Board) -> int:
    h = 0
    for i in range(3):
        for j in range(3):
            if board.state[i][j] != 0:
                x, y = np.where(board.solution == board.state[i][j])
                h += abs(i - x) + abs(j - y)
    return h 


def CB(board: Board) -> int:
    return 

def NA(board: Board) -> int:
    return 

'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    frontier = PriorityQueue()
    frontier.put((heuristic(board), board))
    visited = set()

    while not frontier.empty():
        _, current_state = frontier.get()

        if current_state.goal_test():
            return
        visited.add(current_state)

        next_states = current_state.next_action_states()
        for next_state, action in next_states:
            if str(next_state) not in visited:
                # Calculate the cost of the next state
                cost = current_state.g + 1 + heuristic(next_state)
                print("cost:",cost)
                print("next_state:\n",next_state)
                # Add the next state to the frontier
                frontier.put((cost, next_state))
                
                # Update the cost of the next state
                next_state.g = current_state.g + 1

    return None
