import random

from env import Env
from printing import print_state

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
    P2 = 2
    PLAYER_REWARDS = {
        P1:  1,
        P2: -1
    }

    def __init__(self):
        super().__init__()
        self.state = None
        self.turn = None

    def reset(self):
        self.state = [1 if i < 9 else 0 for i in range(27)]
        self.turn = TicTacToeEnv.P1
        return self.state

    def step(self, action):

        self._validate_action(action)

        self.state[action] = 0
        self.state[action + self.turn * 9] = 1
        self.turn = 3 - self.turn

        TicTacToeEnv._validate_state(self.state)

        reward, done = self._get_reward()
        return self.state, reward, done

    def get_state_action_pairs(self):
        pairs = []
        for action in self.get_actions():
            copy_state = self.state[::]
            copy_state[action] = 0
            copy_state[action + self.turn * 9] = 1
            TicTacToeEnv._validate_state(copy_state)
            pairs.append((action, copy_state))
        return pairs

    def get_actions(self):
        return [i for i in range(9) if self.state[i] == 1]

    def _validate_action(self, action):
        assert self.state[action] == 1 and self.state[action + 9] == 0 and self.state[action + 18] == 0

    @staticmethod
    def _validate_state(s):
        for i in range(9):
            assert s[i] + s[i + 9] + s[i + 18] == 1

    def _get_reward(self):

        for player in [TicTacToeEnv.P1, TicTacToeEnv.P2]:

            for triple in TicTacToeEnv.WINNING_COMBINATIONS:

                if all(self.state[i + 9 * player] == 1 for i in triple):
                    return TicTacToeEnv.PLAYER_REWARDS[player], True

        if all(self.state[i] == TicTacToeEnv.EMPTY for i in range(9)):
            return 0, True

        return 0, False



if __name__ == '__main__':

    env = TicTacToeEnv()
    env.reset()
    while True:
        a = random.choice(env.get_actions())
        s, r, d = env.step(a)
        print_state(s)
        print('Reward: ', r)
        print()
        if d: break
