import time

from games.tictactoe import TicTacToe
from games.connect4 import Connect4
from mcts.uct.uct import uct


if __name__ == '__main__':

    state = Connect4()
    print(state)

    step = 0

    while not state.result()[1]:

        if step % 2 == 1:
            action = int(input('Action: '))
        else:
            start = time.time()
            action = uct(state, n=1000, best=True, verbose=True)
            print(time.time() - start)
        state.act(action)

        print(state)

        step += 1

    print('Result:', state.result()[0])



