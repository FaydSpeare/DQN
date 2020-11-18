from tensorflow import keras

from tictactoe import TicTacToeEnv
from agent import Agent
from printing import print_state



if __name__ == '__main__':

    model = keras.models.load_model('/home/fayd/Fayd/Projects/DQN/models/1605621282.0392525.model')
    env = TicTacToeEnv()
    state = env.reset()
    agent = Agent.load_agent(model)

    output = model.predict([
        [
            -1,  1, -1,
             1,  1,  0,
            -1,  1, -1,
        ]
    ])
    print(output)

    while True:
        print()
        print_state(state)

        first = True
        agent_turn = TicTacToeEnv.P1 if not first else TicTacToeEnv.P2

        if env.turn == agent_turn:
            action = agent.get_best_action(env.get_state_action_pairs(), inverted=first, verbose=True)
        else:
            print("Available Actions:", env.get_actions())
            action = int(input("Action: "))

        state, _, done = env.step(action)

        if done:
            print()
            print_state(state)
            break




