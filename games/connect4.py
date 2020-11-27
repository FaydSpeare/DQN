from typing import Tuple, List
import random
import numpy as np

from games import base
from games.base import BaseGame


WINNING_COMBINATIONS = [
    [0, 1, 2, 3], [1, 2, 3, 4],
    [2, 3, 4, 5], [3, 4, 5, 6],
    [7, 8, 9, 10], [8, 9, 10, 11],
    [9, 10, 11, 12], [10, 11, 12, 13],
    [14, 15, 16, 17], [15, 16, 17, 18],
    [16, 17, 18, 19], [17, 18, 19, 20],
    [21, 22, 23, 24], [22, 23, 24, 25],
    [23, 24, 25, 26], [24, 25, 26, 27],
    [28, 29, 30, 31], [29, 30, 31, 32],
    [30, 31, 32, 33], [31, 32, 33, 34],
    [35, 36, 37, 38], [36, 37, 38, 39],
    [37, 38, 39, 40], [38, 39, 40, 41],
    [0, 7, 14, 21], [7, 14, 21, 28],
    [14, 21, 28, 35], [1, 8, 15, 22],
    [8, 15, 22, 29], [15, 22, 29, 36],
    [2, 9, 16, 23], [9, 16, 23, 30],
    [16, 23, 30, 37], [3, 10, 17, 24],
    [10, 17, 24, 31], [17, 24, 31, 38],
    [4, 11, 18, 25], [11, 18, 25, 32],
    [18, 25, 32, 39], [5, 12, 19, 26],
    [12, 19, 26, 33], [19, 26, 33, 40],
    [6, 13, 20, 27], [13, 20, 27, 34],
    [20, 27, 34, 41], [0, 8, 16, 24],
    [1, 9, 17, 25], [2, 10, 18, 26],
    [3, 11, 19, 27], [7, 15, 23, 31],
    [8, 16, 24, 32], [9, 17, 25, 33],
    [10, 18, 26, 34], [14, 22, 30, 38],
    [15, 23, 31, 39], [16, 24, 32, 40],
    [17, 25, 33, 41], [3, 9, 15, 21],
    [4, 10, 16, 22], [5, 11, 17, 23],
    [6, 12, 18, 24], [10, 16, 22, 28],
    [11, 17, 23, 29], [12, 18, 24, 30],
    [13, 19, 25, 31], [17, 23, 29, 35],
    [18, 24, 30, 36], [19, 25, 31, 37],
    [20, 26, 32, 38]
]


EMPTY = 0
P1 = 1
P2 = -1

def get_result(state):

    for player in [P1, P2]:
        for quad in WINNING_COMBINATIONS:
            if all(state[i] == player for i in quad):
                return player, True

    if all(tile != EMPTY for tile in state):
        return EMPTY, True

    return EMPTY, False

def get_moves(state):
    moves = []
    for col in range(7):
        for row in range(6):
            i = 7 * row + col
            if state[i] == EMPTY:
                moves.append(i)
                break
    return moves

class Connect4(base.BaseGame):

    def __init__(self, state=None, turn=None):
        self.turn = P1 if turn is None else turn
        self.state = [EMPTY for _ in range(42)] if state is None else state

    def simulate(self) -> int:
        turn = self.turn
        state = self.state[::]
        result, done = get_result(state)

        while not done:
            action = random.choice(get_moves(state))
            state[action] = turn
            turn *= -1
            result, done = get_result(state)

        return result

    def get_legal_moves(self) -> List:
        return get_moves(self.state)

    def result(self) -> Tuple[int, bool]:
        return get_result(self.state)

    def act(self, action) -> None:
        self.state[action] = self.turn
        self.turn *= -1

    def copy(self) -> BaseGame:
        return Connect4(state=self.state[::], turn=self.turn)

    def is_terminal(self) -> bool:
        return self.result()[1]

    def to_play(self):
        return self.turn

    def to_nn_input(self):
        game_state = np.zeros((4, 7, 6))
        for idx, tile in enumerate(self.state):
            if tile == 0: game_state[0][idx % 7][idx // 7] = 1
            if tile == -1: game_state[1][idx % 7][idx // 7] = 1
            if tile == 1: game_state[2][idx % 7][idx // 7] = 1
            game_state[3] = np.ones((7, 6)) * self.turn
        return game_state.swapaxes(0, 2)

    def __repr__(self):
        char_map = {0: '-', 1: 'x', -1: 'o'}
        board = ''
        for row in reversed(range(6)):
            for col in range(7):
                i = 7 * row + col
                board += char_map[self.state[i]] + ' '
            board += '\n'
        return board + '\n'