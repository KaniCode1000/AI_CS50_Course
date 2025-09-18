"""
Tic Tac Toe Player
"""

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
    xc = 0
    for i in board:
        for j in i:
            if j == X:
                xc += 1
            elif j == O:
                xc -= 1
    if xc:
        return O
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = set()
    for index,i in enumerate(board):
        for indi,j in enumerate(i):
            if j == EMPTY:
                acts.add((index,indi))
    return acts


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    valid = (0,1,2)
    if action[0] in valid and action[1] in valid:
        copy_board = copy.deepcopy(board)
        move = player(board)
        copy_board[action[0]][action[1]] = move
        return copy_board
    else:
        raise ValueError('Incorrect action')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        #horizontal check
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        #vertical check
        if board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    #main diag check
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    #sec diag check
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] != EMPTY:
        return board[1][1]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None: #if no winner
        for i in board: #check if the game is tied (no valid moves left)
            if EMPTY in i:
                break
        else:
            return True
    else: #there is a winner
        return True
    return False #game left to play

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    final = winner(board)
    if final == None:
        return 0
    elif final == X:
        return 1
    return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #functions
    def max_val(board):
        if terminal(board):
            return utility(board)
        v = -2
        action_set = actions(board)
        for act in action_set:
            v = max(v,min_val(result(board,act)))
        return v
        
    def min_val(board):
        if terminal(board):
            return utility(board)
        v = 2
        action_set = actions(board)
        for act in action_set:
            v = min(v,max_val(result(board,act)))
        return v
    
    play = player(board)
    if terminal(board):
        return None
    action_set = actions(board)
    the_act = None

    if play == X:
        value = -2
        for i in action_set:
            temp_val = min_val(result(board,i))
            if temp_val > value:
                value = temp_val
                the_act = i
    
    else:
        value = 2
        for i in action_set:
            temp_val = max_val(result(board,i))
            # print(play,temp_val)
            if temp_val < value:
                value = temp_val
                the_act = i

    return the_act