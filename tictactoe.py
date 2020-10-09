"""
Tic Tac Toe Player
"""

import math
import copy

# First player "Maximizing player"
X = "X"
# Seconde player "Minimizing player"
O = "O"
# To fill the board
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # How many Xs played
    xs = 0
    # How many Os played
    os = 0
    for i in range(len(board)):
        for j in range(len(board)):
            # Count Os
            if board[i][j] == O:
                os += 1
            # Count Xs
            if board[i][j] == X:
                xs += 1
    # Return the player who has palyed less 
    if os > xs:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set to save all hte position
    pos = set()
    for i in range(len(board)):
        for j in range(len(board)):
            # If the position is empty then we can play in this position
            if board[i][j] == EMPTY:
                pos.add((i, j))
    # Return all the posiible positions
    return pos


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make a copy of the board to let the AI make the calculations
    cop = copy.deepcopy(board)
    # See whose turn it is
    current_player = player(cop)
    row_num = 0
    col_num = 0

    # If the play is not valid raise exception
    if action is None or cop[action[0]][action[1]] is not None:
        raise Exception("INVALID MOVE")

    for row in cop:
        for col in row:
            # Let the AI make its move
            if row_num == action[0] and col_num == action[1]:
                cop[row_num][col_num] = current_player
            col_num += 1
        row_num += 1
        col_num = 0
    # Return the copied board
    return cop


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # ROW
    for i in range(len(board)):
        # If three in a row are equal
        if board[i][0] == board[i][1] == board[i][2]:
            # If it was X return it or O return it
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
    
    # COL
    for j in range(len(board)):
        # If three in a column are eaual
        if board[0][j] == board[1][j] == board[2][j]:
            # If so, return X or O depends on who won
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
    
    # DIGs
    if board[0][0] == board[1][1] == board[2][2]:
        # Check the main diagonal
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    
    if board[0][2] == board[1][1] == board[2][0]:
        # Check the the other diag
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O

    # Return None if no one has won
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If the board is terminal it means the game is over
    # If it's over return Ture, otherwise return False
    if winner(board) is not None:
        return True
    elif len(actions(board)) == 0:
        return True
    else:
        return False
        

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If the winner is X return 1
    if winner(board) == X:
        return 1
    # If the winner is O return -1
    elif winner(board) == O:
        return -1
    # If it's a tie return 0
    else:
        return 0

    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is over return None
    if terminal(board): 
        return None
    
    # Initialize the optimal move
    optimalMove = None

    # Initialize the alpha and beta
    alpha = -math.inf
    beta = math.inf

    # If it's X's turn
    if player(board) == X:
        v = alpha
        # Check all the possible moves
        for action in actions(board):
            # Get the possible the actions of the other player and calculate depends on it
            value_action = min_value(result(board, action), alpha, beta)

            # If there is better move
            if value_action > v:
                v = value_action
                optimalMove = action

    # If it's O's turn
    else:
        v = beta
        # Check all the possible moves
        for action in actions(board):
            # Get the possible the actions of the other player and calculate depends on it
            value_action = max_value(result(board, action), alpha, beta)

            # If there is better move
            if value_action < v:
                v = value_action
                optimalMove = action

    # Return the best move the AI can make
    return optimalMove


def max_value(board, alpha, beta):
    # If the game is over return 1 or -1 or 0 depends on the winner
    if terminal(board): 
        return utility(board)

    v = -math.inf

    # Check all the possible moves
    for action in actions(board):
        # Get the best move
        v = max(v, min_value(result(board, action), alpha, beta))

        # If alpha is higher then beta then there is no point in continuing
        # Because no other value can beat this score
        alpha = max(v, alpha)
        if alpha > beta:
            break

    # Return the best move
    return v
    
def min_value(board, alpha, beta):
    # If the game is over return 1 or -1 or 0 depends on the winner
    if terminal(board): 
        return utility(board)
        
    v = math.inf
    # Check all the possible moves
    for action in actions(board):
        # Get the best move
        v = min(v, max_value(result(board, action), alpha, beta))

        # If alpha is higher then beta then there is no point in continuing
        # Because no other value can beat this score
        beta = min(v, beta)
        if alpha > beta:
            break
        
    # Return the best move
    return v
