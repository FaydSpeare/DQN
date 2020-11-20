import tensorflow as tf
import time

from mcts.env.tictactoe import TicTacToe
from mcts.quct.quct import quct
from mcts.uct.uct import uct

char_map = {0: '-', 1: 'x', -1: 'o'}

if __name__ == '__main__':

    network = tf.keras.models.load_model('/home/fayd/Fayd/Projects/DQN/mcts/models/quct_avg')
    output = network.predict([[
       -1, 1, 1,
       -1,-1, 1,
        0, 0, 0,
        -1
    ]])

    print(output)
    state = TicTacToe()
    step = 0
    print(state)


    while not state.result()[1]:

        if step % 2 == 0:
            #action = int(input('Action: '))
            #state.make_move(action)
            state = uct(state, n=1000, verbose=True, best=True).state
        else:
            start = time.time()
            state = quct(state, network, None, n=1000, verbose=True, best=True).state
            print(time.time() - start)
        step += 1
        print(state)

    result = state.result()[0]
    print(result)

    print()