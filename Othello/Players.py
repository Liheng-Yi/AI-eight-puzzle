import random

class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        bestScore = float('-inf')
        bestMove = None

        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, self.symbol):
                    newBoard = board.cloneOBoard()
                    newBoard.play_move(c, r, self.symbol)
                    score = self.alphabeta(newBoard, depth=1, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=False)
                    if score > bestScore:
                        bestScore = score
                        bestMove = (c, r)

        return bestMove



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """


    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    def alphabeta(self, board, depth=0, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True):
        # terminal state or maximum depth reached
        if depth == self.max_depth or self.terminal_state(board):
            # print("depth == self.max_depth or self.terminal_state(board):")
            return self.eval_board(board)

        if maximizingPlayer:
            maxEval = float('-inf')
            # print("if maxismizingPlayer")
            for successor in self.get_successors(board, self.symbol):
                eval = self.alphabeta(successor, depth+1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                
                if beta <= alpha:
                    break # beta cut-off
            return maxEval
        else: # minimizing player
            minEval = float('inf')
            print("maximizingPlayer")
            for successor in self.get_successors(board, self.flip_symbol(self.symbol)):
                eval = self.alphabeta(successor, depth+1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break # alpha cut-off
            return minEval
        
    def get_move(self, board):
        bestScore = float('-inf')
        bestMove = None

        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, self.symbol):
                    if bestMove is None:  # Assign the first valid move to bestMove
                        bestMove = (c, r)

                    newBoard = board.cloneOBoard()
                    newBoard.play_move(c, r, self.symbol)
                    score = self.alphabeta(newBoard, depth=1, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=False)
                    if score > bestScore:
                        bestScore = score
                        bestMove = (c, r)

        return bestMove


    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        if self.eval_type == 0:
            # Simple strategy: score is difference in number of pieces
            ai_pieces = board.count_score(self.symbol)
            opp_pieces = board.count_score(self.oppSym)
            value = ai_pieces - opp_pieces

        elif self.eval_type == 1:
            value = 1
        elif self.eval_type == 2:
                    # More complex strategy: score is difference in number of pieces, but corners and edges are weighted more heavily
            ai_pieces = 0
            opp_pieces = 0
            for c in range(board.cols):
                for r in range(board.rows):
                    if board.grid[c][r] == self.symbol:
                        # Increase score if AI controls this cell
                        ai_pieces += 1
                        if c == 0 or c == board.cols - 1 or r == 0 or r == board.rows - 1:
                            # Increase score further if this cell is on an edge
                            ai_pieces += 1
                        if (c == 0 and r == 0) or (c == 0 and r == board.rows - 1) or (c == board.cols - 1 and r == 0) or (c == board.cols - 1 and r == board.rows - 1):
                            # Increase score even further if this cell is a corner
                            ai_pieces += 2
                    elif board.grid[c][r] == self.oppSym:
                        # Do the same for the opponent's pieces
                        opp_pieces += 1
                        if c == 0 or c == board.cols - 1 or r == 0 or r == board.rows - 1:
                            opp_pieces += 1
                        if (c == 0 and r == 0) or (c == 0 and r == board.rows - 1) or (c == board.cols - 1 and r == 0) or (c == board.cols - 1 and r == board.rows - 1):
                            opp_pieces += 2

            value = ai_pieces - opp_pieces
        return value


    def get_successors(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = []
        
        # Iterate over all cells on the board
        for c in range(board.cols):
            for r in range(board.rows):
                # If a legal move can be made from this cell
                if board.is_legal_move(c, r, player_symbol):
                    # Create a copy of the current board state
                    successor = board.cloneOBoard()
                    # Make the move on the copied board
                    successor.play_move(c, r, player_symbol)
                    # Add the new board state to the list of successors
                    successors.append(successor)
        
        return successors 


    


        
            





