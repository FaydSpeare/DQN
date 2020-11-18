import tensorflow as tf
import random
import time

from agent import Agent
from tictactoe import TicTacToeEnv



def __create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='softsign')
    ])
    model.compile(loss='mse', optimizer='adam')
    return model

MIN_EPSILON = 0.
EPSILON_DECAY = 0.999
MIN_EPSILON = 0.001

def run():

    agent = Agent(__create_model)
    opponent = agent.duplicate()

    env = TicTacToeEnv()
    results = {
        True: [0, 0, 0],
        False: [0, 0, 0]
    }
    epsilon = 1.0

    for episode in range(10000):

        if episode % 200 == 0:
            print()
            print(f'Episode {episode}. epsilon={round(epsilon, 3)}')
            print(f'Results: {results}/50', )
            win_draw_x = results[True][1] + results[True][2]
            win_draw_o = results[False][1] + results[False][0]
            loss_x = results[True][0]
            loss_o = results[False][2]
            if win_draw_o + win_draw_x > loss_x + loss_o:
                opponent = agent.duplicate()
                print('Updating Opponent')
            results = {
                True: [0, 0, 0],
                False: [0, 0, 0]
            }

        current_state = env.reset()
        step = 0

        # Switch sides
        inverted = bool(episode % 2)
        learning_agent_turn = TicTacToeEnv.P1 if not inverted else TicTacToeEnv.P2

        state_history = []
        action_history = []

        while True:

            if env.turn == learning_agent_turn:

                if random.random() > epsilon:
                    action = agent.get_best_action(env.get_state_action_pairs(), inverted=inverted)
                else:
                    action = random.choice(env.get_actions())

            else:
                action = opponent.get_best_action(env.get_state_action_pairs(), inverted=(not inverted))


            state_history.append(current_state)
            action_history.append(action)

            next_state, reward, done = env.step(action)

            agent.update_replay_memory((current_state, action, 0, next_state, False))
            if done: agent.update_replay_memory((next_state, action, reward, next_state, True))

            agent.train()

            if done:
                results[inverted][reward + 1] += 1
                break

            current_state = next_state
            step += 1

        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

    agent.main_model.save(f'models/{time.time()}.model')






if __name__ == '__main__':
    run()