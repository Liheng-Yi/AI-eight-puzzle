#!/bin/sh
#p1type="human", p2type="minimax", 
#  p1_eval_type=0, p1_prune=False, p2_eval_type=0, p2_prune=False

#python GameDriver.py human human 0 0 0 0 8 8
#python GameDriver.py human alphabeta 0 0 0 0 8 8
sys.argv[1] and sys.argv[2] never changem, wihch stays at alphabeta
for sys.argv[3] and sys.argv[5] will have value 0,1,2
    and sys.argv[7] and sys.argv[8] have 2,4,6,8,10 and 12
    
python3 GameDriver.py alphabeta alphabeta 0 0 0 0 8 8
python3 GameDriver.py alphabeta alphabeta 0 0 0 0 8 8
python3 GameDriver.py alphabeta alphabeta 0 0 0 0 8 8
python3 GameDriver.py alphabeta alphabeta 0 0 0 0 8 8

#p1type="human", p2type="alphabeta",  p1_eval_type=0, p1_prune=False,
#                                     p2_eval_type=0, p2_prune=False, 
#                                     p1_depth=8, p2_depth=8):