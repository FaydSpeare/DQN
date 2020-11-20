import tensorflow as tf

from mcts.tictactoe import TicTacToe
from mcts.quct import quct
from mcts.uct import uct

char_map = {0: '-', 1: 'x', -1: 'o'}

def print_state(state):
    for i in range(3):
        print(char_map[state.state[3*i]] + char_map[state.state[3*i+1]] + char_map[state.state[3*i+2]])
    print()


if __name__ == '__main__':

    network = tf.keras.models.load_model('/home/fayd/Fayd/Projects/DQN/mcts/models/quct_avg')
    output = network.predict([[0,0,0,0,0,0,0,1,1,1]])

    state = TicTacToe()
    step = 0
    print_state(state)


    while not state.result()[1]:

        if step % 2 == 0:
            #action = int(input('Action: '))
            #state.make_move(action)
            state = uct(state, n=100, verbose=True, best=False).state
        else:
            state = quct(state, network, None, n=100, verbose=True, best=False).state
        step += 1
        print_state(state)

    result = state.result()[0]
    print(result)

    print()