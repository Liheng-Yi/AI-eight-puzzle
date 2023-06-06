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
        self.total_nodes_seen += 1
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
        self.total_nodes_seen += 1
        # print("!!!")
        if depth == self.max_depth or self.terminal_state(board):
            # print("depth == self.max_depth or self.terminal_state(board):")
            return self.eval_board(board)
        
        if maximizingPlayer:
            # print("if maxismizingPlayer")
            return self.max_value(board, depth, alpha, beta)
        else:
            return self.min_value(board, depth, alpha, beta)

    def max_value(self, board, depth, alpha, beta):
        maxEval = float('-inf')
        for successor in self.get_successors(board, self.symbol):
            eval = self.alphabeta(successor, depth+1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    def min_value(self, board, depth, alpha, beta):
        minEval = float('inf')
        for successor in self.get_successors(board, self.flip_symbol(self.symbol)):
            eval = self.alphabeta(successor, depth+1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)

            if beta <= alpha:


                break

        return minEval

        
    def calculate_score(self, board, c, r):
        newBoard = board.cloneOBoard()
        newBoard.play_move(c, r, self.symbol)
        if self.prune == 0:
            score = self.alphabeta(newBoard, depth=1, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=False)
        else:
            score = self.minimax(newBoard, depth=1, maximizingPlayer=False)
        return score

    def get_move(self, board):
        bestScore = float('-inf')
        bestMove = None
        for c in range(board.cols):
            for r in range(board.rows):

                if board.is_legal_move(c, r, self.symbol):

                    if bestMove is None:  # Assign the first valid move to bestMove
                        bestMove = (c, r)
                    score = self.calculate_score(board, c, r)
                    
                    if score > bestScore:
                        bestScore = score
                        bestMove = (c, r)
        return bestMove
    

    def minimax(self, board, depth=0, maximizingPlayer=True):
    # terminal state or maximum depth reached
        self.total_nodes_seen += 1
        if depth == self.max_depth or self.terminal_state(board):
            return self.eval_board(board)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for successor in self.get_successors(board, self.symbol):
                eval = self.minimax(successor, depth+1, False)
                maxEval = max(maxEval, eval)
                
            return maxEval
        else: # minimizing player
            minEval = float('inf')
            for successor in self.get_successors(board, self.flip_symbol(self.symbol)):
                eval = self.minimax(successor, depth+1, True)
                minEval = min(minEval, eval)
            return minEval

    def get_legal_moves(self, symbol, board):
        count = 0
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_cell_empty(c, r) and board.is_legal_move(c, r, symbol):
                    count += 1
        return count

    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        tem = self.eval_type
        self.eval_type = int(tem)
        if self.eval_type == 0:
            # Simple strategy: score is difference in number of pieces
            ai_pieces = board.count_score(self.symbol)
            opp_pieces = board.count_score(self.oppSym)
            value = ai_pieces - opp_pieces

        elif self.eval_type == 1:
            my_legal_moves = self.get_legal_moves(self.symbol, board)
            opponent_legal_moves = self.get_legal_moves(self.oppSym, board)
            return my_legal_moves - opponent_legal_moves
        
        elif self.eval_type == 2:
                    # More complex strategy: score is difference in number of pieces, but corners and edges are weighted more heavily
            ai_pieces = 0
            opp_pieces = 0
            for c in range(board.cols):
                for r in range(board.rows):
                    if board.grid[c][r] == self.symbol:
                        ai_pieces += 1
                        if c == 0 or c == board.cols - 1 or r == 0 or r == board.rows - 1:
                            ai_pieces += 1
                        if (c == 0 and r == 0) or (c == 0 and r == board.rows - 1) or (c == board.cols - 1 and r == 0) or (c == board.cols - 1 and r == board.rows - 1):
                            ai_pieces += 2
                    elif board.grid[c][r] == self.oppSym:
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
    
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, player_symbol):
                    successor = board.cloneOBoard()
                    successor.play_move(c, r, player_symbol)
                    successors.append(successor)

        return successors 

