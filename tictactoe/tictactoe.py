"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
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
    x = 0
    o = 0
    for row in board:
        for cell in row:
            if cell == X:
                x += 1
            elif cell == O:
                o += 1
    if not terminal(board) and x == o:
        return X
    elif x > o:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Invalid Move')
    elif terminal(board):
        raise ValueError('Game Over')

    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        for j in range(3):
            horX = (board[i][j] == X) and (board[i][j+1] == X) and (board[i][j+2] == X)
            verX = (board[i][j] == X) and (board[i+1][j] == X) and (board[i+2][j] == X)
            diaX = (board[i][j] == X and board[i+1][j+1] == X and board[i+2][j+2] == X) or (board[i][j+2] == X and board[i+1][j+1] == X and board[i+2][j] == X)

            horO = (board[i][j] == O) and (board[i][j+1] == O) and (board[i][j+2] == O)
            verO = (board[i][j] == O) and (board[i+1][j] == O) and (board[i+2][j] == O)
            diaO = (board[i][j] == O and board[i+1][j+1] == O and board[i+2][j+2] == O) or (board[i][j+2] == O and board[i+1][j+1] == O and board[i+2][j] == O)

            if horX or verX or diaX:
                return X
            elif horO or verO or diaO:
                return O
            else:
                return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    cells_filled = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X or board[i][j] == 0:
                cells_filled += 1

    if cells_filled == 9 or winner(board) != None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == [[EMPTY]*3]*3:
        return (0, 0)

    if player(board) == X:
        plays = []
        for action in actions(board):
            plays.append([minValue(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]

    if player(board) == O:
        plays = []
        for action in actions(board):
            plays.append([maxValue(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0])[0][1]

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, minValue(result(board, action)))
    return v
