"""
This module contains the core TicTacToe simulation class, along with a main 
method to run the game with a human and agent player.
"""

from itertools import cycle
import rules
import numpy as np
import logging
import random
import sys


class TicTacToe(object):
    """
    This class simulates Tic-Tac-Toe (Noughts and Crosses) of size n x n.

    It provides the simulation engine to model the flow of a single game,
    requesting moves from each player in turn and storing the state of the game
    board.

    Attributes:
        board (numpy.ndarray): two dimensional array representing the game board
        players ([Player]): list of game players
        logger (logging.Logger): logger
    """
    def __init__(self, players, n=3, shuffle=False, logger=None):
        # Initialise the board and players
        self.board = np.zeros((n, n))
        self.set_players(players)
        self.logger = logger
        self.shuffle = shuffle

    def set_players(self, players):
        """
        Sets the game players.

        The current game players are replaced with the players specified. Each
        player is assigned a side from the list specified in the rules module.
        The number of players must match the number of sides.

        Args:
            players ([Player]): the list of players

        Raises:
            ValueError: if `players` is not the same length as `rules.sides`
        """
        if len(players) != len(rules.sides):
            raise ValueError("Incorrect number of players, expected {0}.".
                    format(len(rules.sides)))
        for player, side in zip(players, rules.sides):
            player.side = side

        self.__players = players

    def players(self):
        """
        Returns the list of players.

        Returns:
            [Player]: the current list of game players
        """
        return self.__players

    def run(self):
        """
        Executes a single run of the game.

        The board is initially set to empty, then the play method is called to
        request moves from each player until a winner is identified.

        The players are notified that the game is about to start, and again once
        the game has finished.

        Returns:
            int: the side of the winning player, or None if there was a draw
        """
        # Reset the game board
        self.board.fill(rules.EMPTY)

        # Notify the players that the game is starting
        for player in self.players():
            player.start()

        # Play the game
        winner = self.play()

        # Notify the players that the game has finished
        for player in self.players():
            player.finish(winner)

        return winner

    def play(self):
        """
        Plays the game, alternating turns between the players.

        Moves are requested sequentially from each player in turn until there is
        a winner. The moves are checked for validity.

        Returns:
            int: the side of the winning player, or None if there was a draw
        """
        if self.shuffle:
            random.shuffle(self.players())

        player_cycle = cycle(self.players())

        for player in player_cycle:
            # Uncomment to log board state each turn
            # if self.logger:
            #     self.logger.debug(rules.board_str(self.board))

            # Get the coordinates of the player's move
            move = player.move(self.board.copy())

            # Make the move if it is valid
            if rules.valid_move(self.board, move):
                self.board[move] = player.side
            else:
                if self.logger:
                    self.logger.fatal("Invalid move")
                raise ValueError("Not a valid move: {0}".format(move))

            # Check for a win or draw
            if rules.winning_move(self.board, move):
                if self.logger:
                    self.logger.info("{2}\nGame over: {0} win ({1})".format(
                            rules.side_name(player.side), type(player).__name__,
                            rules.board_str(self.board)))
                # Return winning player
                return player.side
            elif rules.board_full(self.board):
                # The board is full so the game concluded with a draw
                if self.logger:
                    self.logger.info("{0}\nGame over: Draw".format(
                        rules.board_str(self.board)))
                # Return None for draw
                return None


def main():
    # Set up the logger
    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
            format="\n%(message)s")

    # Create the players
    from players import Human
    human = Human(logger=logger)
    from agents.minimax import MiniMaxAgent
    agent = MiniMaxAgent(logger=logger)

    # Set up the game
    game = TicTacToe([human, agent], shuffle=True, logger=logger)
    while True:
        game.run()


if __name__ == "__main__":
    main()
