from env import Env

class TicTacToeEnv(Env):

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

    def __init__(self):
        super().__init__()

        self.state = None
        self.turn = None
        self.reset()

    def reset(self):
        self.state = [TicTacToeEnv.EMPTY for i in range(9)]
        self.turn = TicTacToeEnv.P1

    def step(self, action):

        self._validate_action(action)

        self.state[action] = self.turn
        self.turn = TicTacToeEnv.P2 if self.turn == TicTacToeEnv.P1 else TicTacToeEnv.P1

        return self.state, *self._get_reward()


    def get_state_action_pairs(self):
        pairs = []
        for action in self._get_actions():
            copy_state = self.state[::]
            copy_state[action] = self.turn
            pairs.append((action, copy_state))
        return pairs

    def _get_actions(self):
        return [i for i, v in enumerate(self.state) if v == TicTacToeEnv.EMPTY]


    def _validate_action(self, action):
        assert self.state[action] == TicTacToeEnv.EMPTY

    def _get_reward(self):

        for player in [TicTacToeEnv.P1, TicTacToeEnv.P2]:

            for triple in TicTacToeEnv.WINNING_COMBINATIONS:

                if all(self.state[i] == player for i in triple):
                    return player, True

        if all(self.state[i] != TicTacToeEnv.EMPTY for i in range(9)):
            return TicTacToeEnv.EMPTY, True

        return 0, False








if __name__ == '__main__':
    env = TicTacToeEnv()