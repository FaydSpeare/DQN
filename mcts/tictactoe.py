import random

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

class TicTacToe:

    def __init__(self, state=None, turn=None):
        self.state = [EMPTY for _ in range(9)] if state is None else state
        self.turn = P1 if turn is None else turn

    def simulate(self):

        turn = self.turn
        state = self.state[::]
        while not TicTacToe.__result(state)[1]:
            action = random.choice(TicTacToe.get_moves(state))
            state[action] = turn
            turn *= -1

        return TicTacToe.__result(state)[0]

    def get_next_states(self):
        next_states = []
        for action in TicTacToe.get_moves(self.state):
            state = self.state[::]
            state[action] = self.turn
            next_states.append(TicTacToe(state=state, turn=-self.turn))
        return next_states

    def make_move(self, action):
        self.state[action] = self.turn
        self.turn *= -1


    def result(self):
        return TicTacToe.__result(self.state)

    @staticmethod
    def get_moves(state):
        return [i for i, t in enumerate(state) if t == EMPTY]

    @staticmethod
    def __result(state):

        for player in [P1, P2]:
            for triple in WINNING_COMBINATIONS:
                if all(state[i] == player for i in triple):
                    return player, True

        if all(tile != EMPTY for tile in state):
            return EMPTY, True

        return EMPTY, False


