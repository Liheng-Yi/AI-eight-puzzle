from board import Board
import numpy as np
import time
from agent import MT, a_star_search
from agent import CB, a_star_search
from agent import NA, a_star_search
from agent import BF, a_star_search
import pandas as pd
import xlsxwriter
from xlsxwriter import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

def main():

    total_CPU_time = 0.0
    total_node = 0
    total_len = 0
    total_run = 0
    total_success_time = 0
    total_Percentage = 0

    seed_CPU_time = 0.0
    seed_node = 0
    seed_len = 0
    seed_run = 0
    seed_success_time = 0
    seed_Percentage = 0
    node_list = []
    len_list= []
    cpu_list= []
    nodes = 0
    for m in [10,20,30,40,50]:
        node_list = []
        len_list= []
        cpu_list= []
        for seed in range(0,10):

            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            start =  time.process_time()

            solution = a_star_search(board, BF)
            
            end =  time.process_time()
            solution_cpu_time = end-start
            seed_CPU_time += solution_cpu_time
            seed_node += nodes

            node_list.append(nodes)
            len_list.append(len(solution))
            cpu_list.append(solution_cpu_time)
            # print(f"Seed: {seed}, Solution len: {len(solution)}, CPU time: {solution_cpu_time:.4f} seconds, nodes: {nodes}")
        print("when m = ", m)
        average = sum(node_list) / len(node_list)
        print("average number of nodes :", average)
        average = sum(len_list) / len(len_list)
        print("average solution len:", average)      
        average = sum(cpu_list) / len(cpu_list)
        print("cpu time:", average,"\n")   


    
    # data = {"Node": node_list, "len_list": len_list, "cpu_list": cpu_list}
    
    # df = pd.DataFrame([node_list, [12, 22, 32], [31, 32, 33]],
    #               index=['one', 'two', 'three'], columns=['a', 'b', 'c'])
    # # create a dataframe from the data

    # # Create an Excel workbook object
    # wb = Workbook()

    # # Select the active worksheet
    # ws = wb.active

    # # Write the DataFrame to the worksheet
    # for r in dataframe_to_rows(df, index=False, header=True):
    #     ws.append(r)

    # # Save the workbook as an Excel file with UTF-8 encoding
    # wb.save('results.xlsx')
    # print("Data written to Excel file successfully.")
if __name__ == "__main__":
    main()