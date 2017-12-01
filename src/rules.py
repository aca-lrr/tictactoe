"""
This module contains methods defining the rules of the game.
"""
import numpy as np
import rules


EMPTY = 0
NOUGHT = 1
CROSS = -1
sides = [CROSS, NOUGHT]
__tokens = {EMPTY: " ", NOUGHT: "o", CROSS: "x"}
__names = {EMPTY: " ", NOUGHT: "Noughts", CROSS: "Crosses"}


def token(value):
    """Returns the game token for a value."""
    try:
        return __tokens[value]
    except KeyError:
        return "?"


def side_name(value):
    """Returns the side name for a value."""
    try:
        return __names[value]
    except KeyError:
        return "?"


def opponent(side):
    """Returns the side of the opponent."""
    return -side


def empty_cells(board):
    """
    Returns a list of the empty cells remaining on a board.

    Args:
        board (numpy.ndarray): two dimensional array representing the game board

    Returns:
        numpy.ndarray: an array containing the locations of empty cells as
            x,y pairs
    """
    # Get list of empty cells and transpose into a list of x,y pairs
    return np.transpose(np.nonzero(board == rules.EMPTY))


def valid_move(board, move):
    """
    Returns whether the move is valid for the given board, i.e. whether it is
    one of the empty cells.

    Args:
        board (numpy.ndarray): two dimensional array representing the game board
        move ((int, int)): tuple with the coordinates of the new move (x, y)

    Returns:
        bool: True if the move is valid, False otherwise
    """
    return list(move) in rules.empty_cells(board).tolist()


def winning_move(board, move):
    """
    Checks whether the given move resulted in a win.

    Calculates the sum of the row, column and diagonals of the new move and
    compares against the expected value for a full line. A full line sums to n 
    or -n if the sides are 1 and -1

    Args:
        board (numpy.ndarray): two dimensional array representing the board
            after the move
        move ((int, int)): tuple with the coordinates of the new move (x, y)

    Returns:
        bool: True if the move resulted in a win, False otherwise
    """
    n = board.shape[0]
    x, y = move

    # Row
    if abs(board[x].sum()) == n:
        return True
    # Column
    elif abs(board[:,y].sum()) == n:
        return True
    # Diagonal
    elif x == y and abs(board.diagonal().sum()) == n:
        return True
    # Anti-diagonal
    elif x == (n - 1) - y and abs(np.fliplr(board).diagonal().sum()) == n:
        return True
    else:
        return False


def board_full(board):
    """
    Checks whether a given board is full, i.e. there are no empty spaces left 
    for moves.

    Args:
        board (numpy.ndarray): two dimensional array representing the board

    Returns:
        bool: True if the board is full, False otherwise
    """
    return EMPTY not in board


def board_str(board):
    """
    Formats a board as a string replacing cell values with enum names.

    Args:
        board (numpy.ndarray): two dimensional array representing the board
            after the move

    Returns:
        str: the board represented as a string
    """
    # Join columns using '|' and rows using line-feeds
    return str('\n'.join(['|'.join([rules.token(item) for item in row])
            for row in board]))
