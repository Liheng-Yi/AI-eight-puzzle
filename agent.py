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
    frontier.put((heuristic(board), board, []))
    visited = set()

    while not frontier.empty():
        f, state, path = frontier.get()
        if state.goal_test():
            return path
        for neighbor, action in state.get_successors():
            if neighbor not in visited:
                g = len(path) + 1
                h = heuristic(neighbor)
                f = g + h
                frontier.put((f, neighbor, path + [action]))

    return None
