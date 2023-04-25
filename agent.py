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

    times = 10

    while not frontier.empty() and times > 0:
        _, current_state = frontier.get()
        # print("intitial: \n", current_state.initial_state)
        # print("current_state: \n", current_state.state,"\n")

        if current_state.check_solution(current_state.total_action):
            print("we got this!!!!!!!!!!!, \n current map:\n", current_state)

            return current_state.total_action

        visited.add(tuple(map(tuple, current_state.state)))

        next_states = current_state.next_action_states()
        print("current state: \n", tuple(map(tuple, current_state.state)))
        # print("visited: \n", visited)
        print("current cost", current_state.g)
        for next_state, action in next_states:


            if tuple(map(tuple, next_state.state)) not in visited:
                # Calculate the cost of the next state
                cost = current_state.g + heuristic(next_state)
                # print("cost:",cost)
                # print("action:", action)
                print("next state: \n", tuple(map(tuple, next_state.state)))
                # print("visited: \n", visited)
                print("next_state cost", cost)
                # print("visited",visited)
                # print("next_state:\n",str(next_state))

                # Add the next state to the frontier
                frontier.put((cost, next_state))

                # Update the cost of the next state
                next_state.g = current_state.g + 1
                # append action
                next_state.total_action.append(action)

        times = times - 1

    return None
