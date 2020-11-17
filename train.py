import tensorflow as tf
import random
import time

from agent import Agent
from tictactoe import TicTacToeEnv



def __create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16),
        tf.keras.layers.Dense(1)
    ])
    model.compile(loss='mse', optimizer='adam')
    return model

MIN_EPSILON = 0.
EPSILON_DECAY = 0.999
MIN_EPSILON = 0.001

def run():

    agent = Agent(__create_model)
    env = TicTacToeEnv()
    results = 0
    epsilon = 0.5

    for episode in range(500):



        current_state = env.reset()
        step = 0

        if episode % 50 == 0:
            print(f'Episode {episode}. epsilon={round(epsilon, 3)}')
            print(f'Results: {results}/50', )
            print()
            results = 0

        while True:

            if env.turn == TicTacToeEnv.P1:

                if random.random() > epsilon:
                    action = agent.get_best_action(env.get_state_action_pairs())
                else:
                    action = random.choice(env.get_actions())

                next_state, reward, done = env.step(action)

                agent.update_replay_memory((current_state, action, reward, next_state, done))
                agent.train()

                if done:
                    results += reward
                    break


            # Random Player
            else:

                action = random.choice(env.get_actions())
                next_state, reward, done = env.step(action)

            current_state = next_state
            step += 1

        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

    agent.main_model.save(f'models/{time.time()}.model')






if __name__ == '__main__':
    run()