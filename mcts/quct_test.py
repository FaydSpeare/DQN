import tensorflow as tf
import time

from games.tictactoe import TicTacToe
from mcts.quct.quct import quct

char_map = {0: '-', 1: 'x', -1: 'o'}

if __name__ == '__main__':

    network = tf.keras.models.load_model('/home/fayd/Fayd/Projects/DQN/mcts/models/quct_avg')


    game = TicTacToe()
    step = 0
    print(game)


    while not game.is_terminal():

        if step % 2 == 1:
            action = int(input('Action: '))
        else:
            start = time.time()
            action = quct(game, network, None, n=50, verbose=True, best=True)
            print(time.time() - start)

        game.act(action)
        step += 1
        print(game)

    result = game.result()[0]
    print(result)

    print()