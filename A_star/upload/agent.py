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


def CB(board):

    n = board.state.shape[0]
    total_conflicts = 0
    for row in board.state:
        row_conflicts = helper(row)
        total_conflicts += row_conflicts
    for i in range(n):
        col = board.state[:, i]
        col_conflicts = helper(col)
        total_conflicts += col_conflicts
    
    return total_conflicts

def helper(row):
    conflicts = 0
    non_zero_values = [val for val in row if val != 0]
    
    for i, val in enumerate(non_zero_values):
        for other_val in non_zero_values[i+1:]:
            if val > other_val:
                conflicts += 1
                
    return conflicts



def NA(board: Board) -> int:
    def count_conflicts_in_row(row):
        conflicts = 0
        max_val = -1
        for i, val in enumerate(row):
            if val == 0:
                continue
            if val > max_val:
                max_val = val
            else:
                for j in range(i + 1, len(row)):
                    if row[j] == 0:
                        continue
                    if row[j] == max_val:
                        break
                    if row[j] < max_val and row[j] > val:
                        conflicts += 1
        return conflicts
    def count_conflicts(board):
        total_conflicts = 0
        for i in range(3):
            row_conflicts = count_conflicts_in_row(board[i, :])
            col_conflicts = count_conflicts_in_row(board[:, i])
            total_conflicts += row_conflicts + col_conflicts
        return total_conflicts
    
    return count_conflicts(board.state) + CB(board)



def BF(board: Board) -> int:
    
    return 0

'''
A* Search 
'''


def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    frontier = PriorityQueue()
    frontier.put((heuristic(board), board))
    visited = set()
    num_node = 0
    #times = 100

    while not frontier.empty():# and times > 0:
        _, current_state = frontier.get()

        visited.add(tuple(map(tuple, current_state.state)))
        
        next_states = current_state.next_action_states()

        for next_state, action in next_states:
            next_state.nodes =  next_state.nodes + 1
            num_node = num_node +1
            if tuple(map(tuple, current_state.state)) == tuple(map(tuple, current_state.solution)):
                return (current_state.total_action)

            if tuple(map(tuple, next_state.state)) not in visited:
                # Calculate the cost of the next state
                cost = current_state.g + heuristic(next_state)
                frontier.put((cost, next_state))
                next_state.g = current_state.g + 1
                next_state.total_action.append(action)

        #times = times - 1

    return None