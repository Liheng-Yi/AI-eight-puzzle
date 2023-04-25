from __future__ import annotations
from board import Board
from collections.abc import Callable
from queue import PriorityQueue
import numpy as np


def MT(board: Board) -> int:
    h = 0
    for i in range(3):
        for j in range(3):
            if board.state[i][j] != 0 and board.state[i][j] != board.solution[i][j]:
                h += 1
    return h


def CB(board: Board) -> int:
    '''
    Counts the number of conflicts in the board's rows and columns
    '''
    n = board.state.shape[0]
    total_conflicts = 0
    
    for i in range(n):
        row = board.state[i]
        col = board.state[:, i]
        
        # Count conflicts in row
        row_conflicts = 0
        for j in range(n):
            if row[j] != 0:
                for k in range(j + 1, n):
                    if row[k] != 0 and row[j] > row[k]:
                        row_conflicts += 1
        
        # Count conflicts in column
        col_conflicts = 0
        for j in range(n):
            if col[j] != 0:
                for k in range(j + 1, n):
                    if col[k] != 0 and col[j] > col[k]:
                        col_conflicts += 1
        
        # Add total conflicts for row and column to total conflicts for board
        total_conflicts += row_conflicts + col_conflicts
    
    return total_conflicts



def NA(board: Board) -> int:
    '''
    Counts the number of conflicts in the board's rows and columns
    '''
    n = board.state.shape[0]
    total_conflicts = 0
    
    for i in range(n):
        row = board.state[i]
        col = board.state[:, i]
        
        # Count conflicts in row
        row_conflicts = 0
        for j in range(n):
            if row[j] != 0:
                for k in range(j + 1, n):
                    if row[k] != 0 and row[j] > row[k]:
                        row_conflicts += 1
        
        # Add total conflicts for row and column to total conflicts for board
        total_conflicts += row_conflicts
    
    return total_conflicts



'''
A* Search 
'''


def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    frontier = PriorityQueue()
    frontier.put((heuristic(board), board))
    visited = set()

    #times = 100

    while not frontier.empty():# and times > 0:
        _, current_state = frontier.get()
        # print("intitial: \n", current_state.initial_state)
        # print("current_state: \n", current_state.state,"\n")


        visited.add(tuple(map(tuple, current_state.state)))

        next_states = current_state.next_action_states()
        # print("visited: \n", visited)
        for next_state, action in next_states:

            if tuple(map(tuple, current_state.state)) == tuple(map(tuple, current_state.solution)):
                return current_state.total_action

            if tuple(map(tuple, next_state.state)) not in visited:
                # Calculate the cost of the next state
                cost = current_state.g + heuristic(next_state)

                # Add the next state to the frontier
                frontier.put((cost, next_state))

                # Update the cost of the next state
                next_state.g = current_state.g + 1
                # append action
                next_state.total_action.append(action)

        #times = times - 1

    return None