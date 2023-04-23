from board import Board
import numpy as np
import time
from agent import MT, a_star_search

def main():

    for m in [10,20,30,40,50]:
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            start =  time.process_time()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            solution = a_star_search(board, MT)
            end =  time.process_time()
            solution_cpu_time = end-start


            print(f"Board: {board.state}, Seed: {seed}, Solution: {solution}, CPU time: {solution_cpu_time:.4f} seconds")

if __name__ == "__main__":
    main()
