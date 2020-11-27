import random
import numpy as np
from games import base

WINNING_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

EMPTY = 0
P1 = 1
P2 = -1


def get_result(state):

    for player in [P1, P2]:
        for triple in WINNING_COMBINATIONS:
            if all(state[i] == player for i in triple):
                return player, True

    if all(tile != EMPTY for tile in state):
        return EMPTY, True

    return EMPTY, False


def get_moves(state):
    return [i for i in range(9) if state[i] == EMPTY]


class TicTacToe(base.BaseGame):

    def __init__(self, state=None, turn=None):
        self.state = [EMPTY for _ in range(9)] if state is None else state
        self.turn = P1 if turn is None else turn

    def get_legal_moves(self):
        return get_moves(self.state)

    def act(self, action):
        self.state[action] = self.turn
        self.turn *= -1

    def copy(self):
        return TicTacToe(state=self.state[::], turn=self.turn)

    def simulate(self):

        turn = self.turn
        state = self.state[::]
        result, done = get_result(state)

        while not done:
            action = random.choice(get_moves(state))
            state[action] = turn
            turn *= -1
            result, done = get_result(state)

        return result

    def result(self):
        return get_result(self.state)

    def to_nn_input(self):
        game_state = np.zeros((4, 3, 3))
        for idx, tile in enumerate(self.state):
            if tile == 0: game_state[0][idx % 3][idx // 3] = 1
            if tile == -1: game_state[1][idx % 3][idx // 3] = 1
            if tile == 1: game_state[2][idx % 3][idx // 3] = 1
            game_state[3] = np.ones((3, 3)) * self.turn
        return game_state.swapaxes(0, 2)

    def is_terminal(self) -> bool:
        return self.result()[1]

    def to_play(self):
        return self.turn

    def __repr__(self):
        char_map = {0: '-', 1: 'x', -1: 'o'}
        s = ''
        for i in range(3):
            s += char_map[self.state[3 * i]] + char_map[self.state[3 * i + 1]] + char_map[self.state[3 * i + 2]] + '\n'
        return s + '\n'



'''
    def get_next_states(self):
        next_states = []
        for action in get_moves(self.state):
            state = self.state[::]
            state[action] = self.turn
            next_states.append(TicTacToe(state=state, turn=-self.turn))
        return next_states
'''
