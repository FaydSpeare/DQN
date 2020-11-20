import tensorflow as tf
import random
import time

from agent import Agent
from tictactoe import TicTacToeEnv



def __create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='softsign')
    ])
    model.compile(loss='mse', optimizer='adam')
    model.build((None, 27))
    return model

MIN_EPSILON = 0.
EPSILON_DECAY = 0.996
MIN_EPSILON = 0.1
START_EPSILON = 1.

def run():



    agent = Agent(__create_model)
    past_agent = agent.duplicate()

    env = TicTacToeEnv()
    epsilon = START_EPSILON

    for self_play_step in range(40):

        print('Starting Self-Play Step:', self_play_step)
        print('Epsilon:', epsilon)
        results = [0, 0, 0]

        for episode in range(50):

            current_state = env.reset()
            step = 0

            state_history = []
            action_history = []

            while True:

                state_action_pairs = env.get_state_action_pairs()

                if random.random() > epsilon:
                    action = agent.get_best_action(state_action_pairs, inverted=(step % 2 == 1))
                else:
                    action = random.choice(env.get_actions())

                state_history.append(current_state)
                action_history.append(action)

                next_state, reward, done = env.step(action)

                if step > 0:
                    agent.update_replay_memory((state_history[-2], action_history[-2], reward, next_state, done))
                    if done: agent.update_replay_memory((current_state, action, reward, next_state, done))

                #agent.update_replay_memory((current_state, action, reward, next_state, done))
                agent.train()

                if done:
                    results[reward + 1] += 1
                    break

                current_state = next_state
                step += 1

            epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

        print(f'Results: {results}\n')

        print('Testing Against Random - X')
        results = [0, 0, 0]
        for episode in range(20):
            env.reset()
            step = 0
            while True:
                if step % 2 == 0: action = agent.get_best_action(env.get_state_action_pairs())
                else: action = random.choice(env.get_actions())
                _, reward, done = env.step(action)
                if done:
                    results[reward + 1] += 1
                    break
                step += 1
        print(f'Results: {results}')

        print('Testing Against Random - O')
        results = [0, 0, 0]
        for episode in range(20):
            env.reset()
            step = 0
            while True:
                if step % 2 == 1: action = agent.get_best_action(env.get_state_action_pairs(), inverted=True)
                else: action = random.choice(env.get_actions())
                _, reward, done = env.step(action)
                if done:
                    results[reward + 1] += 1
                    break
                step += 1
        print(f'Results: {results}')

        print()







    agent.main_model.save(f'models/{time.time()}.model')






if __name__ == '__main__':
    run()