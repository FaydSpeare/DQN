from mcts.tictactoe import TicTacToe
from mcts.uct import uct

char_map = {0: '-', 1: 'x', -1: 'o'}

def print_state(state):
    for i in range(3):
        print(char_map[state.state[3*i]] + char_map[state.state[3*i+1]] + char_map[state.state[3*i+2]])
    print()


if __name__ == '__main__':

    state = TicTacToe()
    print_state(state)

    step = 0

    while not state.result()[1]:

        if step % 2 == 0:
            #action = int(input('Action: '))
            #state.make_move(action)
            state = uct(state).state
        else:
            state = uct(state).state




        print_state(state)

        step += 1

    print('Result:', state.result()[0])



