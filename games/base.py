from __future__ import annotations
import abc
from typing import Tuple, List


class BaseGame(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def simulate(self) -> int:
        """ Simulates a game and return the result """
        pass

    @abc.abstractmethod
    def get_legal_moves(self) -> List:
        """ Gets a list of the legal moves that can be made """
        pass

    @abc.abstractmethod
    def result(self) -> Tuple[int, bool]:
        """
        Returns the result of the game where the int indicates the result and the bool
        indicates whether or not the game is over.
        """
        pass

    @abc.abstractmethod
    def act(self, action) -> None:
        """ Perform the specified action """
        pass

    @abc.abstractmethod
    def copy(self) -> BaseGame:
        """ Create a deep copy of the game """
        pass

    @abc.abstractmethod
    def is_terminal(self) -> bool:
        """ Returns whether or not the game is over """
        pass

    @abc.abstractmethod
    def to_play(self):
        pass

    @abc.abstractmethod
    def to_nn_input(self):
        pass



