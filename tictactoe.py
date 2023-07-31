"""
Tic Tac Toe Player
"""

import math
import copy

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
    if board:
        countX = 0 
        countO = 0
        for row in board:
            countX += row.count(X)
            countO += row.count(O)
            
        if (countX > countO):
            return O
        else:
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionstmp = []
    if board:
        for row in range(3):
            for col in range(3):
                if (board[row][col] == EMPTY):
                    actionstmp.append((row,col))

    return actionstmp


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    if (board[action[0]][action[1]] == EMPTY):
        if player(board) == X:
            result[action[0]][action[1]] = X
            return result
        else:
            result[action[0]][action[1]] = O
            return result
    else:
        raise Exception("Not Valid Move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check diagonals
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2])  \
        or (board[2][0] == board[1][1] and board[1][1] == board[0][2]):
        return board[1][1]

    #Check rows
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O  
    #Check columns
    for col in range(3):
        if all(row[col] == X for row in board):
            return X
        elif all(row[col] == O for row in board):
            return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        countEmpty = 0
        for row in board:
            countEmpty += row.count(EMPTY)
        if countEmpty > 0:
            return False
        else:
            return True


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
    depth = 0
    best_move = getNodeValue(board,player(board),depth, None, -1000000, 1000000)[1]

    return best_move




def getNodeValue(board, play, depth, next_move, alpha, beta):
    #terminal codition by depth
    #terminal condition by the rules
    if terminal(board):
        return utility(board) , None, beta, alpha

    moves = actions(board)

    #intermediate node
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = copy.deepcopy(board)
        newBoard[move[0]][move[1]] = play
        childrenNodes.append(newBoard)
    
    #prunning
    if (play == X): #turn of max
        nodeValue = -100000000
    else:              #turn of min
        nodeValue = 100000000
        
        
    childrenValues = []
    next_move_index = -1
    curent_child_index = 0
    for child in childrenNodes: #goes deeper into the tree to get the values that come to this node
        call = getNodeValue(child, X if play == O else O, depth+1, next_move, alpha, beta)
        value = call[0]
        childrenValues.append(value)
        bottomUPAlpha = call[3] #beta propagates to alpha
        bottomUPBeta = call[2]  #alpha propagates to beta
    
        if (play == X): #turn of max
            if bottomUPAlpha > alpha:
                alpha = bottomUPAlpha
            alpha = max(alpha, value)
            if (value > nodeValue):
                next_move_index = curent_child_index
                nodeValue = value
            if(nodeValue >= beta):
                break
            
        else:              #turn of min
            if bottomUPBeta < beta:
                beta = bottomUPBeta
            beta = min(beta, value)
            if (value < nodeValue):
                next_move_index = curent_child_index
                nodeValue = value
            if(nodeValue <= alpha):
                    break
                
        curent_child_index = curent_child_index + 1
    
    
    if depth == 0:
        next_move = moves[next_move_index]
    
    return nodeValue, next_move, alpha, beta